from django.db import models
from .base_models import BaseModel
from .git_models import GitTb
from .project_models import Project


# 应用服务，相当于一个可独立部署的微服务
class App(BaseModel):
    cn_name = models.CharField(max_length=255, verbose_name="中文名")
    app_id = models.IntegerField(default=0, verbose_name="应用编号")
    git = models.ForeignKey(GitTb,
                            related_name="ra_app",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="Git实例")
    git_app_id = models.IntegerField(default=0, verbose_name="Git应用ID")
    git_trigger_token = models.CharField(max_length=64,
                                         blank=True,
                                         null=True,
                                         verbose_name="git trigger token")
    project = models.ForeignKey(Project,
                                related_name='ra_project',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='项目')
    build_script = models.CharField(max_length=255,default='build.sh', verbose_name="编译脚本名")
    deploy_script = models.CharField(max_length=255, default='bifang.sh', verbose_name="部署脚本名")
    zip_package_name = models.CharField(max_length=255, default='demo.zio', verbose_name="应用压缩包")
    service_port = models.IntegerField(default=0, verbose_name="服务端口")
    service_username = models.CharField(max_length=24,
                                        blank=True,
                                        null=True,
                                        verbose_name="执行用户名")
    service_group = models.CharField(max_length=24,
                                     blank=True,
                                     null=True,
                                     verbose_name="执行用户组")
    op_log_no = models.IntegerField(default=0, verbose_name="启停日志次数")

    class Meta:
        db_table = 'App'
        verbose_name = 'App应用'
        verbose_name_plural = 'App应用'
