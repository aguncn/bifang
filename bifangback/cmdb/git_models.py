from django.db import models
from .base_models import BaseModel


# GitLab代码仓库地址，有的公司可能有多个Git仓库，所以独立出一个数据表
# 如果只有一个代码仓库，当然也可以直接在django的settings文件里定义
class GitTb(BaseModel):
    # gitlab的URL
    git_url = models.URLField(verbose_name="Git API地址")
    # 用于python的gitlab库去进行API 认证时需要
    git_token = models.CharField(max_length=64, default='no_token', verbose_name="Git API认证token")
    # gitlab的版本，仅于展示记录，无实在用途
    git_ver = models.CharField(max_length=16, default='12.10', verbose_name="Git版本")

    class Meta:
        # 用于定义数据表名称，而不使用系统自动生成的
        db_table = 'GitTb'
        # 用一起定义admin后台显示名称(规则为数据表名及简短中文)
        verbose_name = 'GitTb代码仓库'
        verbose_name_plural = 'GitTb代码仓库'
