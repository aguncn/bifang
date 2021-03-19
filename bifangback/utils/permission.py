from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from cmdb.models import Project
from cmdb.models import App
from cmdb.models import Permission


# 判断是否为管理员组
def is_admin_group(user):
    try:
        user_groups = Group.objects.filter(user=user)
        print("user groups, ", user_groups)
    except ObjectDoesNotExist as e:
        print(e)
        return False
    for user_group in user_groups:
        if user_group.name == 'admin':
            return True
    return False


# 判断是否为Project管理员
def is_project_admin(project_id, user):
    project = Project.objects.get(id=project_id)
    if user == project.create_user or is_admin_group(user):
        return True
    return False


# 判断是否为APP管理员
def is_app_admin(app_id, user):
    app = App.objects.get(id=app_id)
    if user == app.create_user or is_admin_group(user):
        return True
    return False


# 获取APP管理员
def get_app_admin(app_id):
    return App.objects.get(id=app_id).create_user


# 获取APP的各个权限的相关成员
def get_app_user(app_id, action_id):
    filter_dict = dict()
    filter_dict['app__id'] = app_id
    filter_dict['action__id'] = action_id
    permission_set = Permission.objects.get(**filter_dict)
    user_set = permission_set.pm_user.all()
    return user_set


# 判断是否具有APP的相关环境的相关权限
def is_right(app_id, action_id, user):
    # 是管理员，可直接具有相关权限
    if is_app_admin(app_id, user):
        return True
    filter_dict = dict()
    filter_dict['app__id'] = app_id
    filter_dict['action__id'] = action_id
    try:
        permission_set = Permission.objects.filter(**filter_dict)
        for permission in permission_set:
            if user == permission.pm_user:
                return True
        return False
    except Permission.DoesNotExist as e:
        print(e)
        return False
