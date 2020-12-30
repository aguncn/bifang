from django.db import models
from django.contrib.auth import get_user_model
from .base_models import BaseModel
from .git_models import GitTb
from .project_models import Project

User = get_user_model()


# 应用服务，相当于一个可独立部署的微服务
class App(BaseModel):
    app_id = models.IntegerField(default=0, verbose_name="应用编号")
    git = models.ForeignKey(GitTb,
                            related_name="ra_deploy_app",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="Git实例")
    git_repo = models.CharField(max_length=255,
                                verbose_name="Git地址")
    project = models.ForeignKey(Project,
                                related_name='ra_project',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='项目')
    service_username = models.CharField(max_length=24, blank=True, null=True, verbose_name="执行用户名")
    service_group = models.CharField(max_length=24, blank=True, null=True, verbose_name="执行用户组")
    op_log_no = models.IntegerField(default=0, verbose_name="启停日志次数")

    class Meta:
        db_table = 'App'
        verbose_name = 'App应用'
        verbose_name_plural = 'App应用'
