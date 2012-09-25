

from django.contrib import admin
from models import LogFiles

class LogFilesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(LogFiles, LogFilesAdmin)
