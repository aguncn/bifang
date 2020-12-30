from django.db import models
from django.contrib.auth import get_user_model
from .base_models import BaseModel
from .app_models import App
from .env_models import Env

User = get_user_model()

IS_INC_TOT_CHOICES = (
    ('TOT', r'增量'),
    ('INC', r'全量'),
)

DEPLOY_TYPE_CHOICES = (
    ('deployall', r'发布所有'),
    ('deploypkg', r'发布程序'),
    ('deploycfg', r'发布配置'),
    ('rollback', r'回滚'),
)


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
    git_commit = models.CharField(max_length=255,
                                  blank=True,
                                  null=True)
    salt_path = models.CharField(max_length=255,
                                 verbose_name="Salt APP路径")
    nginx_url = models.URLField(default=None,
                                blank=True,
                                null=True,
                                verbose_name="Nginx路径")
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
