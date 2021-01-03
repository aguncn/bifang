from django.db import models
from .base_models import BaseModel
from django.contrib.auth import get_user_model
from .app_models import App

User = get_user_model()


# 创建编译发布单， 部署发布单两个大的权限
class Action(BaseModel):
    action_id = models.IntegerField(unique=True, verbose_name="权限序号")

    class Meta:
        db_table = 'Action'
        verbose_name = 'Action权限'
        verbose_name_plural = 'Action权限'


class Permission(BaseModel):
    app = models.ForeignKey(App,
                            related_name="ra_permission",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="App应用")
    action = models.ForeignKey(Action,
                               related_name="ra_permission",
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name="操作权限")
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
