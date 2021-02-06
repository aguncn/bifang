from django.db import models
from .base_models import BaseModel


# 项目，可表示由多个相关微服务组成的项目
# 比如，istio里的bookin就算是bifang中的一个project
# 而其中的productpage,reviews,details,ratings这些应用，就相当于bifang中的app应用
class Project(BaseModel):
    # 只是为了一个中文显示，及统一的项目id加的。不解释
    cn_name = models.CharField(max_length=255, verbose_name="中文名")
    project_id = models.IntegerField(default=0, verbose_name="项目编号")

    class Meta:
        db_table = 'Project'
        verbose_name = 'Project项目'
        verbose_name_plural = 'Project项目'
