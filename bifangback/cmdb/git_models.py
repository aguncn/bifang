from django.db import models
from .base_models import BaseModel


# Git代码仓库地址，有的公司可能有多个Git仓库
class GitTb(BaseModel):
    git_url = models.URLField(verbose_name="Git API地址")
    git_token = models.CharField(max_length=64, default='no_token', verbose_name="Git API认证token")
    git_ver = models.CharField(max_length=16, default='12.10', verbose_name="Git版本")

    class Meta:
        db_table = 'GitTb'
        verbose_name = 'GitTb代码仓库'
        verbose_name_plural = 'GitTb代码仓库'
