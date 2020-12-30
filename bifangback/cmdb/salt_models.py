from django.db import models
from .base_models import BaseModel


# Sat Api地址，不同环境，可能需要不同的Salt Master隔离
class SaltTb(BaseModel):
    salt_url = models.URLField(verbose_name="Git API地址")
    username = models.CharField(max_length=64, verbose_name="Git API用户")
    password = models.CharField(max_length=64, verbose_name="Git API密码")
    token = models.CharField(max_length=64, verbose_name="Git API认证token")

    class Meta:
        db_table = 'SaltTb'
        verbose_name = 'SaltTb远程执行工具'
        verbose_name_plural = 'SaltTb远程执行工具'
