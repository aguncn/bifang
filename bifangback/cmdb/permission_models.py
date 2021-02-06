from django.db import models
from .base_models import BaseModel
from django.contrib.auth.models import User
from .app_models import App


# 创建编译发布单， 环境流转，部署发布单三个大的权限，
# bifang暂不支持基于各个具体环境的细致权限
# 大家可以自己基于书上教授的技能，自行实现
class Action(BaseModel):
    action_id = models.IntegerField(unique=True, verbose_name="权限序号")

    class Meta:
        db_table = 'Action'
        verbose_name = 'Action权限'
        verbose_name_plural = 'Action权限'


# 具体的权限数据表
# 如果要获取某个服务的所有权限，或是某一应用的指定权限的用户列表，都是OK的。
class Permission(BaseModel):
    # 权限与app应用级别关联
    app = models.ForeignKey(App,
                            related_name="ra_permission",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="App应用")
    # 权限与具体的权限动作(创建编译，环境流转，部署发布)关联
    action = models.ForeignKey(Action,
                               related_name="ra_permission",
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name="操作权限")
    # 权限关联到用户
    pm_user = models.ForeignKey(User,
                                related_name="ra_permission",
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name="权限用户")

    class Meta:
        db_table = 'Permission'
        verbose_name = 'Permission应用权限'
        verbose_name_plural = 'Permission应用权限'
