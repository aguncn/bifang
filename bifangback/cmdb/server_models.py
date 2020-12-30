from django.db import models
from .base_models import BaseModel

SYSTEM_CHOICES = (
    ('WINDOWS', 'WINDOWS'),
    ('LINUX', 'LINUX'),
)


# 部署服务器，保证ip和port结合起来的唯一性，可以一个服务器上部署多个应用
class Server(BaseModel):
    ip = models.IPAddressField(max_length=64, verbose_name="服务器Ip")
    port = models.IntegerField(verbose_name="服务器端口")
    system_type = models.CharField(max_length=16,
                                   choices=SYSTEM_CHOICES,
                                   default='LINUX',
                                   verbose_name="操作系统")

    class Meta:
        db_table = 'Server'
        verbose_name = 'Server服务器'
        verbose_name_plural = 'Server服务器'
