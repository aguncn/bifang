from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *

admin.site.site_header = '毕方(BiFang)自动化部署系统'
admin.site.site_title = '登录毕方(BiFang)系统后台'
admin.site.index_title = '毕方(BiFang)后台管理'


class GitTbHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'git_url', 'git_ver']
    history_list_display = ["status"]
    search_fields = ['name', 'git_url']


admin.site.register(GitTb, GitTbHistoryAdmin)
admin.site.register(SaltTb, SimpleHistoryAdmin)
admin.site.register(Env, SimpleHistoryAdmin)
admin.site.register(Project, SimpleHistoryAdmin)


class AppHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'app_id', 'cn_name', 'git_app_id', 'zip_package_name', 'service_port', 'op_no']
    history_list_display = ["status"]
    search_fields = ['name', 'cn_name']


admin.site.register(App, AppHistoryAdmin)
admin.site.register(ServerStatus)


class ServerHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name',  'ip', 'port', 'system_type', 'env', 'main_release', 'back_release']
    history_list_display = ["status"]
    search_fields = ['name', 'ip', 'port']
    readonly_fields = ('create_date', 'update_date')


admin.site.register(Server, ServerHistoryAdmin)
admin.site.register(ReleaseStatus)


class ReleaseHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'env', 'app', 'release_status', 'deploy_no', 'create_user',  'create_date',  'update_date', ]
    history_list_display = ["status"]
    search_fields = ['name']
    readonly_fields = ('create_date', 'update_date')


admin.site.register(Release, ReleaseHistoryAdmin)


class ReleaseHistoryHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'release', 'env', 'release_status', 'deploy_type', 'log_no', 'log']
    history_list_display = ["status"]
    search_fields = ['name', 'release', 'log']
    readonly_fields = ('create_date', 'update_date')


admin.site.register(ReleaseHistory, ReleaseHistoryHistoryAdmin)


class ServerHistoryHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'server',  'release', 'env', 'op_type', 'action_type', 'log_no', 'log']
    history_list_display = ["status"]
    search_fields = ['name', 'release', 'log']
    readonly_fields = ('create_date', 'update_date')


admin.site.register(ServerHistory, ServerHistoryHistoryAdmin)


class PermissionHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name',  'app', 'action', 'pm_user']
    history_list_display = ["status"]
    search_fields = ['name', 'app', 'action']
    readonly_fields = ('create_date', 'update_date')


admin.site.register(Action)
admin.site.register(Permission, PermissionHistoryAdmin)
