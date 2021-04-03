from django.db import models
from .base_models import BaseModel
from .env_models import Env
from .release_models import Release, ReleaseStatus
from .server_models import Server

# 用于在发布单的部署代码层次内的记录，是部署新代码，还是回滚老代码？
# 用于发布单历史
DEPLOY_CHOICES = (
    ('deploy', '部署'),
    ('rollback', '回滚'),
)

# 用于大的方向，是在部署代码，还是单纯在维护服务器启停？
# 用于服务器操作历史，区分发布单和服务器操作历史是有意义的，维护不一样，但也可以一追到底
OP_CHOICES = (
    ('deploy', '部署'),
    ('maintenance', '启停维护'),
)

# 在服务器上操作的第一步作记录，后期根据需要，有可能作维护改动
# 它主要要能包括所有deploy过程中的action_list列表项目
ACTION_CHOICES = (
    ('fetch', '获取软件'),
    ('stop', '停止'),
    ('stop_status', '停止状态检测'),
    ('deploy', '部署'),
    ('rollback', '回滚'),
    ('start', '启动'),
    ('start_status', '启动状态检测'),
    ('health_check', '服务健康检测'),
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
    release_status = models.ForeignKey(ReleaseStatus,
                                      related_name='ra_release_history',
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name="发布单状态")
    deploy_type = models.CharField(max_length=255,
                                   choices=DEPLOY_CHOICES,
                                   blank=True,
                                   null=True,
                                   verbose_name="部署类型")
    # 发布单的次数和这里匹配，即可找到合适的历史记录。
    log_no = models.IntegerField(blank=True,
                                 null=True,
                                 default=0,
                                 verbose_name="部署批次")
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
    # 发布单或app应用的次数和这里匹配，即可找到合适的历史记录。
    log_no = models.IntegerField(blank=True,
                                 null=True,
                                 default=0,
                                 verbose_name="部署启停批次")
    log = models.TextField(verbose_name="日志内容")

    class Meta:
        db_table = 'ServerHistory'
        verbose_name = 'ServerHistory服务器历史'
        verbose_name_plural = 'ServerHistory服务器历史'
