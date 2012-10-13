"""
Logging for:

"""
import os
import re
import linecache

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
        fobj = open(file_full_path, 'rb')
        return fobj

    def get_file_lines_count(self, file_obj):
        """Creates fake log file list (without real lines, but with proper length)"""
        fake_log_file = []
        log_file_fake_lines = file_obj.xreadlines()
        count = 0
        for line in log_file_fake_lines:
            fake_log_file.append(count)
            count += 1
        if fake_log_file:
            fake_log_file.append(count)
        return fake_log_file

    def compile_re_index(self, regexp=None):
        """Creating Regexp prog to match entries"""
        if not regexp:
            regexp = LOG_FILES_RE
        prog = re.compile(regexp)
        return prog

    def parse_log_file(self, logfile, from_line=0, to_line=LOG_FILES_PAGINATE_LINES, full=False):
        """Returns parsed read file

        in form of entry names header (taken from Rgex group names)
        and lines tuples list"""
        file_dict = []
        prog = self.compile_re_index()
        # Reading amount of lines
        line_num = from_line
        if full:
            file_obj = self.get_file(logfile)
            to_line = self.get_file_lines_count(file_obj).__len__()
        for count in range(to_line):
            try:
                line = linecache.getline(logfile, line_num)
                matches_set = prog.findall(str(line))
                file_dict.append(matches_set)
                line_num += 1
            except IndexError:
                # log file is shorter then LOG_FILES_PAGINATE_LINES or
                # amount of lines smaller then from_line left
                pass
        return file_dict

    def compile_header_from_regexp(self, regexp=None):
        """Making logfile indexes header"""
        prog = self.compile_re_index()
        header_length = prog.groups
        header_list = []
        if prog.groupindex:
            for number in range(header_length):
                header_list.append(number)
            for group_name, index in prog.groupindex.iteritems():
                header_list[int(index) - 1] = group_name
        return header_list

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
