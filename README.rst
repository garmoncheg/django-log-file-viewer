# Django Log File Viewer.

Useful to add log files view functionality to your Django admin web site.
Instead of using database log files storage, it gives you ability to store/view log files through GUI.
It requires a directory with Django log files to function. E.g. directory structure:

    $ project_dir/logs/:
       applog.log
       applog.log.2012-09-22
       ...
       errors.log
       applog.log.2012-09-22
       ...

To parse/display these log files you need:

## 1. Install an app and add it to your settings.py INSTALLED_APPS section:

    # settings.py
    INSTALLED_APPS = (
        ...
        'django-log-file-viewer',
        ...
    )

## 2. Set UP 2 django variables in settings.py:

    # settings.py:

    LOG_FILES_DIR = '/path/to/your/log/directory'
        Relative or static path string of your log files directory.
        I recommend using more pythonic way of defining tis with os module. E.g. :

        # settings.py:
        LOG_FILES_DIR = os.path.join(APP_PATH, 'testdata', 'log')

        where APP_PATH is your app's/project's path.

    LOG_FILES_RE = /
        '(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s\[(?P<type>[A-Z]+)\]\s(?P<message>.+)'

        Is a regex to parse your log file against.
        It completely depends of your Django logging settings.
        And table column names (in a parsed logfile)
        depend from group names you provide in the regexp.
        E.g. for Django logging server to parse with this regexp
        you need to have log, as in example
        django_log_file_viewer/testdata/testing.log file.

        to produce this log I've added this formatter to my website.
                'formatters': {
                        'verbose': {
                            'format': '%(asctime)s [%(levelname)s] %(message)s'
                        },
                    },


## 3. And add urls to your main urls section:

    # urls.py
    urlpatterns = patterns('',

        # Include this before admin to enable app admin url overrides
        # Note url must be the same as admin
        # This is required step
        url(r'^admin/', include('django-log-file-viewer.admin_urls')),
        url(r'^admin/', include(admin.site.urls)),

        # To view with custom views:
        # Optional step
        # Will ad urls like www.example.com/logfiles/
        url(r'', include('django-log-file-viewer.urls')),
    )


## TODO's:

* Add pagination to both log files list and log file content

## Reference:

* [Ref] Info on how to add/config logging for your Django based website here:
  https://docs.djangoproject.com/en/dev/topics/logging/ (Official Django documentation)
* [Ref] Parsing/testing Regexp is useful with:
  http://gskinner.com/RegExr/ (real time regexp testing)
