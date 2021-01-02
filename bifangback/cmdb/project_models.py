from django.db import models
from .base_models import BaseModel


# 项目，可表示由多个相关微服务组成的项目
class Project(BaseModel):
    cn_name = models.CharField(max_length=255, verbose_name="中文名")
    project_id = models.IntegerField(default=0, verbose_name="项目编号")

    class Meta:
        db_table = 'Project'
        verbose_name = 'Project项目'
        verbose_name_plural = 'Project项目'
