"""
Author = Meet Shah
After validating post request, controll will transfer to this class to read uploaded csv and append category column in it.
This code assumes that column number 4{ column 0 being base column} is always going to be complaint title.

source :  Read only headers from csv file
            => https://stackoverflow.com/questions/24962908/how-can-i-read-only-the-header-column-of-a-csv-file-using-python
"""
import random

import pandas as pd
from django.conf import settings
import os
import operator

# from .ML_model.ClassificationService import ClassificationService
from Prediction.ML_model.model.ClassificationService import ClassificationService
from Prediction.ML_model.SpeakUp.Model.SpeakupClassificationService import ClassificationService_speakup


class CSV_FILE:
    filename = ''
    username = ''
    group = ''

    def __init__(self, file_name, user_name, company):
        self.filename = file_name
        self.username = user_name
        self.group = company

    def check_csvfile_header(self):
        PATH = os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "input", self.filename)
        try:
            csvfile = pd.read_csv(PATH, nrows=1, encoding="utf-8").columns
        except Exception as e:
            print("Error in checking header")
            print(e)
        Company_Columns = []
        category_list = []
        if self.group == "ICMC":
            try:

                if not hasattr(self.cs, 'get_top_3_cats_with_prob'):
                    self.cs = ClassificationService()
            except Exception as e:
                print(e)
                self.cs = ClassificationService()

            Company_Columns = settings.ICMC_HEADERS
            category_list = settings.ICMC_CATEGORY_LIST

        elif self.group == "SpeakUP":
            try:
                if not hasattr(self.cs, 'get_top_3_cats_with_prob'):
                    self.cs = ClassificationService_speakup()

            except Exception as e:
                print(e)
                self.cs = ClassificationService_speakup()

            Company_Columns = settings.SPEAKUP_HEADERS
            category_list = settings.SPEAKUP_CATEGORY_LIST

        if len(csvfile) == len(Company_Columns):
            for i in range(len(Company_Columns)):
                if Company_Columns[i].strip() == csvfile[i].strip():
                    continue
                else:
                    print("BLA" + Company_Columns[i] + "bla" + csvfile[i])

                    return False, []
            return True, category_list
        else:
            print(csvfile)
            print("Length of csv file: " + str(len(csvfile)))
            print("Length of prefix column: " + str(len(Company_Columns)))
            return False, []

    def delete(self):
        PATH = os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "input", self.filename)
        os.remove(PATH)

    def write_file(self, correct_category):
        csvfile = pd.read_csv(os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "input", self.filename), sep=',',
                              header=0)
        csvfile.insert(loc=0, column='Predicted_Category', value=correct_category)

        csvfile.to_csv(os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "output", self.filename), sep=',',
                       encoding='utf-8', index=False)

        # making difference file
        csvfile = pd.read_csv(os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "output", "Difference.csv"),
                              sep=',',
                              header=0)
        csvfile.insert(loc=0, column='Chosen_category', value=correct_category)

        csvfile.to_csv(
            os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "output", "Difference of " + self.filename),
            sep=',',
            encoding='utf-8', index=False)

    def Read_file(self):
        # encoding='utf-8' for mgcm
        # csvfile = pd.read_csv("./media/" +self.filename, sep=',', header=0)
        csvfile = pd.read_csv(settings.MEDIA_ROOT + "/" + self.username + "/CSV/input" + "/" + self.filename, sep=',',
                              header=0, encoding='utf-8')
        # print(csvfile.columns)

        Dict_List = []
        description = []
        cat1 = []
        cat2 = []
        cat3 = []
        cnt = 0
        for row in csvfile.iterrows():
            dict = {}
            index, data = row
            dict['index'] = index
            # cats = {'category1':80, 'category2':10, 'category3':10}
            if self.group == "ICMC":
                complaint_title = data['complaint_title']
                complaint_description = data['complaint_description']
                description.append(complaint_description)
                dict['problem_description'] = complaint_description
                try:
                    cats = self.cs.get_top_3_cats_with_prob(complaint_title)

                except Exception as e:
                    print("Complaint, ", complaint_title)
                    break
                    # print(cats.encode("utf-8"), "\n")

            elif self.group == "SpeakUP":
                complaint_title = str(data['text'])
                # temp_list = (random.randint(1, 5))
                # dict['emotion'] = temp_list

                if complaint_title != 'nan':
                    dict['problem_description'] = complaint_title
                    description.append(complaint_title)
                    cats = self.cs.get_top_3_cats_with_prob(complaint_title)

                else:
                    description.append("Problem description not found")
                    dict['problem_description'] = "Problem description not found"
                    cats = {'None': 1}

                    # dict['emotion'] = 0
                    # print("Error input: ", complaint_title, " index: ", index)
                    # break

            for k in cats:
                cats[k] = int(cats[k] * 100)
                if k == 'मॅनहोलमध्ये व्यक्ती पडणे':
                    # cats["Person falling in Manhole"] = cats.pop('मॅनहोलमध्ये व्यक्ती पडणे')
                    temp = cats[k]
                    cats["Person falling in Manhole"] = temp / 100
                    del cats['मॅनहोलमध्ये व्यक्ती पडणे']

                elif k == 'थकबाकी येणे बाकी':
                    # cats["Outstanding dues pending"] = cats.pop('मॅनहोलमध्ये व्यक्ती पडणे')
                    temp = cats[k]
                    cats["Outstanding dues pending"] = temp / 100
                    del cats['थकबाकी येणे बाकी']

            sorted_cats = sorted(cats.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_cats)
            cat1.append(sorted_cats[0][0])
            cat2.append(sorted_cats[1][0])
            cat3.append(sorted_cats[2][0])

            dict['category'] = sorted_cats
            # print(dict['category'])
            Dict_List.append(dict)
            # print(Dict_List)

        df = pd.DataFrame({'Predicted category 1': cat1, 'Predicted category 2': cat2, 'Predicted category 3': cat3,
                           'Complaint Description': description})

        df.to_csv(os.path.join(settings.MEDIA_ROOT, self.username, "CSV", "output", "Difference.csv"), sep=',',
                  encoding='utf-8', index=False)

        del self.cs
        return Dict_List, csvfile.shape[0]
