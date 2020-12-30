from django.db import models
from .base_models import BaseModel


# Git代码仓库地址，有的公司可能有多个Git仓库
class GitTb(BaseModel):
    git_url = models.URLField(verbose_name="Git API地址")
    username = models.CharField(max_length=64, verbose_name="Git API用户")
    password = models.CharField(max_length=64, verbose_name="Git API密码")
    token = models.CharField(max_length=64, verbose_name="Git API认证token")

    class Meta:
        db_table = 'GitTb'
        verbose_name = 'GitTb代码仓库'
        verbose_name_plural = 'GitTb代码仓库'
