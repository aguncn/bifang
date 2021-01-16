from django.db import models
from .base_models import BaseModel
from .app_models import App
from .env_models import Env


class ReleaseStatus(BaseModel):
    # Create, Build, Ready, Ongoing,  Success, Failed
    status_value = models.CharField(max_length=1024, blank=True, verbose_name="状态值")

    class Meta:
        db_table = 'ReleaseStatus'
        verbose_name = 'ReleaseStatus发布单状态'
        verbose_name_plural = 'ReleaseStatus发布单状态'


class Release(BaseModel):
    app = models.ForeignKey(App,
                            related_name='ra_release',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="应用")
    env = models.ForeignKey(Env,
                            related_name="ra_release",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    deploy_no = models.IntegerField(blank=True,
                                    null=True,
                                    default=0,
                                    verbose_name="部署次数")
    git_branch = models.CharField(max_length=255,
                                  blank=True,
                                  null=True)
    pipeline_id = models.IntegerField(default=0)
    pipeline_url = models.URLField(default='http://www.demo.com')
    deploy_script_url = models.URLField(default=None,
                                        blank=True,
                                        null=True,
                                        verbose_name="部署脚本路径")
    zip_package_url = models.URLField(default=None,
                                      blank=True,
                                      null=True,
                                      verbose_name="压缩制品库路径")
    deploy_status = models.ForeignKey(ReleaseStatus,
                                      related_name='ra_release',
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name="发布单状态")

    class Meta:
        db_table = 'Release'
        verbose_name = 'Release发布单'
        verbose_name_plural = 'Release发布单'
