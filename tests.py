"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
from django.test import TestCase
from models import LogFilesManager
from settings import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class LogFilesManagerTests(TestCase):
    def test_read_certain_log_file_lines(self):
        manager = LogFilesManager()
        files_list = manager.list_logfiles(LOG_FILES_DIR)
        logfile = manager.get_file(os.path.join(LOG_FILES_DIR, files_list[int(0)]))
        file_len, header_list, file_dict = manager.parse_log_file(logfile, from_line=100)
        print file_dict
