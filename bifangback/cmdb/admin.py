from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *

admin.site.site_header = '毕方(BiFang)自动化部署系统'
admin.site.site_title = '登录毕方(BiFang)系统后台'
admin.site.index_title = '毕方(BiFang)后台管理'


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
admin.site.register(Action)
admin.site.register(Permission, SimpleHistoryAdmin)
