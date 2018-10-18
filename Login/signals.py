"""
Author = Meet Shah

Date:    03/04/2018

Title:   Signal Processing

Version: 1.0

Purpose: The following code is written for automatically creating directory for each new User which is being
registered in database. Further this directories will be used to store files uploaded by user(ie: CSV FILE,
images for speak up etc). Right now this code is written assuming that username of each user entered in database will
be unique and thus so there will be no conflict in the name of directory. In future, if requirement changes then
please add logic of checking whether directory already exists or not and then create new directory.

         The hierarchy of directory will be:

         Project(VenterDjango)-> DATA -> {USERNAME} -> CSV -> INPUT
                                                           -> OUTPUT
                                                    -> *

Source: 1) I learned how to write signals in django from this link: https://www.youtube.com/watch?v=lxSZevvkcc4&t=226s

        2) From the link mentioned below, I learned how to maintain the structure of signals.py file. The link also gives insight on why putting signal code in
           model file is bad idea.
           https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html

Notes:  * => indicates that you can create new directory according to type of data which you want to store. For eg: for storing graphical file you can write code for creating
             image directory and then store all image file in that directory.
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import os


@receiver(post_save, sender=User)
def create_user_directory(sender, **kwargs):
    uname = kwargs['instance'].username
    data_directory_root = settings.MEDIA_ROOT
    path = os.path.join(data_directory_root, uname, "CSV")
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(os.path.join(path, "input")):
        os.makedirs(os.path.join(path, "input"))

    if not os.path.exists(os.path.join(path, "output")):
        os.makedirs(os.path.join(path, "output"))
