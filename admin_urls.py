from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^django_log_file_viewer/logfiles/$', logfiles_list, {'template_name': 'logfiles_admin.html'}, name='log-files-list-admin'),
    url(r'^django_log_file_viewer/logfiles/(?P<logfile_id>\d+)/$', logfile_view, {'template_name': 'logfile_admin.html'}, name='log-file-admin'),
    url(r'^django_log_file_viewer/logfiles/(?P<logfile_id>\d+)/csv$', logfile_to_csv, name='log-file-to-csv-admin'),
)