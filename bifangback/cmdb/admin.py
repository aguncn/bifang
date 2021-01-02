from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


class EnvHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "name"]
    history_list_display = ["status"]
    search_fields = ['name', 'user__username']


admin.site.register(GitTb, SimpleHistoryAdmin)
admin.site.register(SaltTb, SimpleHistoryAdmin)
admin.site.register(Env, SimpleHistoryAdmin)
admin.site.register(Project)
admin.site.register(App)
admin.site.register(Server)
admin.site.register(ReleaseStatus)
admin.site.register(Release)
admin.site.register(ReleaseHistory)
admin.site.register(ServerHistory)
