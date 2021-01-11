from django.db import models
from .base_models import BaseModel
from .env_models import Env
from .release_models import Release, ReleaseStatus
from .server_models import Server

OP_CHOICES = (
    ('deploy', '部署'),
    ('rollback', '回滚'),
    ('maintenance', '启停维护'),
)

ACTION_CHOICES = (
    ('stop', '停止'),
    ('start', '启动'),
    ('restart', '重启'),
)


# 发布单历史，记录发布单的生命周期，新建，编译，流转，部署，回滚部署
class ReleaseHistory(BaseModel):
    release = models.ForeignKey(Release,
                                related_name='ra_release_history',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='发布单')
    env = models.ForeignKey(Env,
                            related_name="ra_release_history",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    deploy_status = models.ForeignKey(ReleaseStatus,
                                      related_name='ra_release_history',
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name="发布单状态")
    op_type = models.CharField(max_length=255,
                               choices=OP_CHOICES,
                               blank=True,
                               null=True,
                               verbose_name="操作类型")
    log = models.TextField(verbose_name="日志内容")

    class Meta:
        db_table = 'ReleaseHistory'
        verbose_name = 'ReleaseHistory发布单历史'
        verbose_name_plural = 'ReleaseHistory发布单历史'


# 服务器变更历史，记录服务器上的部署，停止，回滚
class ServerHistory(BaseModel):
    server = models.ForeignKey(Server,
                               related_name='ra_server_history',
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL,
                               verbose_name='服务器')
    release = models.ForeignKey(Release,
                                related_name='ra_server_history',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='发布单')
    env = models.ForeignKey(Env,
                            related_name="ra_server_history",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    op_type = models.CharField(max_length=255,
                               choices=OP_CHOICES,
                               blank=True,
                               null=True,
                               verbose_name="操作类型")
    action_type = models.CharField(max_length=255,
                                   choices=ACTION_CHOICES,
                                   blank=True,
                                   null=True,
                                   verbose_name="服务器操作类型")
    log = models.TextField(verbose_name="日志内容")

    class Meta:
        db_table = 'ServerHistory'
        verbose_name = 'ServerHistory服务器历史'
        verbose_name_plural = 'ServerHistory服务器历史'
