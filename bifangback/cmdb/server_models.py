from django.db import models
from .base_models import BaseModel
from .app_models import App
from .release_models import Release
from .env_models import Env

SYSTEM_CHOICES = (
    ('WINDOWS', 'WINDOWS'),
    ('LINUX', 'LINUX'),
)


# 部署服务器，保证ip和port结合起来的唯一性，可以一个服务器上部署多个应用
# 当然，能在同一个服务器上，部署多个相同的应用，这得益于将部署脚本让开发自己维护。
# 真正的devops团队，是需要都有开发和运维的跨界实力的啦~
class Server(BaseModel):
    # GenericIPAddressField的字段，让这里只存储ip地址
    ip = models.GenericIPAddressField(max_length=64, verbose_name="服务器Ip")
    # 服务端口，其实，这里是需要优化的，
    # 如果有的服务启动，不提供端口服务呢？乱写么？如何保证多个无端口服务不冲突？
    port = models.IntegerField(verbose_name="服务器端口")
    system_type = models.CharField(max_length=16,
                                   choices=SYSTEM_CHOICES,
                                   default='LINUX',
                                   verbose_name="操作系统")
    # 此服务器与哪一个app关联
    app = models.ForeignKey(App,
                            related_name='ra_server',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name='应用服务')
    # 环境关联，在部署时，根据环境关联服务器
    env = models.ForeignKey(Env,
                            related_name="ra_server",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    # 保存在此服务器正在运行的app的最近发布单
    main_release = models.ForeignKey(Release,
                                     related_name='ra_server_main',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='主发布单')
    # 保存在此服务器正在运行的app的次新发布单，主要用于回滚，bifang只支持最近一次回滚，不支持无限回滚
    back_release = models.ForeignKey(Release,
                                     related_name='ra_server_back',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='备份发布单')

    class Meta:
        db_table = 'Server'
        # 一个服务器上，部署多个应用，保证Ip加port的唯一性。
        unique_together = ('ip', 'port')
        verbose_name = 'Server服务器'
        verbose_name_plural = 'Server服务器'
