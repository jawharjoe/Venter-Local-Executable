from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as f
from django.conf import settings


class upload_file_form(forms.Form):
    """
    Author: Meet Shah, Shivam Sharma
    Source:  This link helped me to write validation code
             https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
    """
    # The attrs is an in built parameter for the FileInput in the form.
    file = forms.FileField(label='Choose CSV File', widget=forms.FileInput(attrs={'accept': ".csv", "id": "filename"}))

    def clean_file(self):
        content = self.cleaned_data['file']
        filename = str(content)
        max_size = int(settings.MAX_UPLOAD_SIZE)
        upload_file_size = int(
            content.size)  # This code might give a buffer error so find a good solution for this. Look at the source link for reference

        # Validating the format of the file
        if filename.endswith('.csv'):
            # Check for the file size of the uploaded file with the max size (12 MB)
            if upload_file_size > max_size:
                # Beware, the ugettext_lazy might not work for python 3.5 and below. It's better to use f strings with Python 3.6 and above. The latest version, the better.
                raise forms.ValidationError(f('Please keep file size under %s. Current file size is %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size))) # filesizeformat is an in built function. Check it's documentation
        else:
            raise forms.ValidationError(f('Please Upload Csv File Only !!!'))
        return content
