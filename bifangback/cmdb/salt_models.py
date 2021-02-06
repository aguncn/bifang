from django.db import models
from .base_models import BaseModel


# Sat Api地址，不同环境，可能需要不同的Salt Master隔离
# 同样，如果只有一个salt master，只需要在django settings文件里定义
class SaltTb(BaseModel):
    # bifang项目主要使用了saltypie这个第三方库操作salt-api，之前的字段，主要是满足saltypie的认证salt-api的参数
    salt_url = models.URLField(verbose_name="Salt API地址")
    salt_user = models.CharField(max_length=64, verbose_name="Salt API用户")
    salt_pwd = models.CharField(max_length=64, verbose_name="Salt API密码")
    eauth = models.CharField(max_length=64, default='pam', verbose_name="Salt API用户认证")
    trust_host = models.BooleanField(default=True, verbose_name="Salt API安全认证")
    # 同样，这个版本只用于可能的展示，现在没有使用
    salt_ver = models.CharField(max_length=12, default='2019.3010', verbose_name="Salt版本")

    class Meta:
        db_table = 'SaltTb'
        verbose_name = 'SaltTb远程执行工具'
        verbose_name_plural = 'SaltTb远程执行工具'
