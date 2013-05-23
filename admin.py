

from django.contrib import admin
from models import LogFile


class LogFileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(LogFile, LogFileAdmin)
