from django.db import models
from .base_models import BaseModel


# 开发环境 ，测试环境，线上环境，灾备环境
class Env(BaseModel):
    env_id = models.IntegerField(default=0, verbose_name="环境Id")

    class Meta:
        db_table = 'Env'
        verbose_name = 'Env环境'
        verbose_name_plural = 'Env环境'
