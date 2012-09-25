# Default settings for the app override in your settings.py
from django.conf import settings
import os

APP_PATH = os.path.abspath(os.path.split(__file__)[0])
LOG_FILES_DIR = getattr(
    settings,
    'LOG_FILES_DIR',
    os.path.join(APP_PATH, 'testdata', 'log')
)
LOG_FILES_RE = getattr(
    settings,
    'LOG_FILES_RE',
    '(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s\[(?P<type>[A-Z]+)\]\s(?P<message>.+)'
)

__all__ = ['LOG_FILES_DIR', 'LOG_FILES_RE',]