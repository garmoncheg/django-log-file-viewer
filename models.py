"""
Logging for:

"""
import os
import re

from django.db import models

from settings import *

class LogFilesManager(object):

    def list_logfiles(self, path):
        """Returns list of files in provided path"""
        file_list = []
        # List only files
        for root,directory,files in os.walk(path):
            for file in files:
                # List only readable files
                try:
                    fi = open(os.path.join(path, file))
                    fi.close()
                    file_list.append(file)
                except Exception:
                    pass
        return file_list

    def get_file(self, file_full_path):
        fobj = open(file_full_path)
        return fobj

    def parse_log_file(self, logfile):
        """Returns parsed read file

        in form of entry names header (taken from Rgex group names)
        and lines tuples list"""
        # Reading file
        logfile.seek(0)
        read_file = logfile.readlines()
        # Creating Regexp prog to match entries
        file_dict = []
        prog = re.compile(LOG_FILES_RE)
        for line in read_file:
            matches_set = prog.findall(str(line))
            file_dict.append(matches_set)
        # Making logfile indexes header
        header_length = prog.groups
        header_list = []
        if prog.groupindex:
            for number in range(header_length):
                header_list.append(number)
            for group_name, index in prog.groupindex.iteritems():
                header_list[int(index) - 1] = group_name
        return (header_list, file_dict)

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class LogFiles(models.Model):
    """Hack object to be added to Django admin"""
    class Meta:
        app_label = string_with_title("django_log_file_viewer", "Django Log Files")
    verbose_name = 'Django Log File'
    verbose_name_plural = 'Django Log Files'
