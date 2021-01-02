from django.db import models
from .base_models import BaseModel
from .salt_models import SaltTb


# 开发环境 ，测试环境，线上环境，灾备环境
class Env(BaseModel):
    env_id = models.IntegerField(default=0, verbose_name="环境Id")
    salt = models.ForeignKey(SaltTb,
                             related_name="ra_env",
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL,
                             verbose_name="Salt地址")

    class Meta:
        db_table = 'Env'
        verbose_name = 'Env环境'
        verbose_name_plural = 'Env环境'
