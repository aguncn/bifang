from django.db import models
from .base_models import BaseModel
from .salt_models import SaltTb


# 开发环境 ，线上环境，等等
class Env(BaseModel):
    # 因为继续自BaseModel，所以name,description,user,date那些字段都有了，不用重复
    # 使用id，可以在必要时，减少一些对数据表自增id的依赖，在作数据库迁移方面，还是有好处的
    env_id = models.IntegerField(default=0, verbose_name="环境Id")
    # 一般salt master都是分环境建的，这样能达到批量管理的目的，多套saltmaster又可以隔离安全网络
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
