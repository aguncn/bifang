from django.db import models
from .base_models import BaseModel


# Sat Api地址，不同环境，可能需要不同的Salt Master隔离
class SaltTb(BaseModel):
    salt_url = models.URLField(verbose_name="Salt API地址")
    salt_user = models.CharField(max_length=64, verbose_name="Salt API用户")
    salt_pwd = models.CharField(max_length=64, verbose_name="Salt API密码")
    salt_token = models.CharField(max_length=64, default='no_token', verbose_name="Salt API认证token")
    is_secure = models.BooleanField(default=True, verbose_name="Salt启用安全")
    salt_ver = models.CharField(max_length=12, default='2019.3010', verbose_name="Salt版本")

    class Meta:
        db_table = 'SaltTb'
        verbose_name = 'SaltTb远程执行工具'
        verbose_name_plural = 'SaltTb远程执行工具'
