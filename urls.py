from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^logfiles/$', logfiles_list, name='logfiles_list'),
    url(r'^logfiles/(?P<logfile_id>\d+)$', logfile_view, name='logfile_view'),
)
