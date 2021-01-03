from django.db import models
from .base_models import BaseModel
from .app_models import App
from .release_models import Release

SYSTEM_CHOICES = (
    ('WINDOWS', 'WINDOWS'),
    ('LINUX', 'LINUX'),
)


# 部署服务器，保证ip和port结合起来的唯一性，可以一个服务器上部署多个应用
class Server(BaseModel):
    ip = models.GenericIPAddressField(max_length=64, verbose_name="服务器Ip")
    port = models.IntegerField(verbose_name="服务器端口")
    system_type = models.CharField(max_length=16,
                                   choices=SYSTEM_CHOICES,
                                   default='LINUX',
                                   verbose_name="操作系统")
    app = models.ForeignKey(App,
                            related_name='ra_server',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name='应用服务')
    main_release = models.ForeignKey(Release,
                                     related_name='ra_server_main',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='主发布单')
    back_release = models.ForeignKey(Release,
                                     related_name='ra_server_back',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='备份发布单')

    class Meta:
        db_table = 'Server'
        unique_together = ('ip', 'port')  # 一个服务器上，部署多个应用，保证Ip加port的唯一性。
        verbose_name = 'Server服务器'
        verbose_name_plural = 'Server服务器'
