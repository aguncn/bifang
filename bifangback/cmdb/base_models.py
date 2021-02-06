from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User


# 基础虚类，所有Model的共同字段，其它model由此继承，包括记录orm操作历史的history字段。
class BaseModel(models.Model):
    # unique=True用于保证名称不重复
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="名称")
    description = models.CharField(max_length=100,
                                   null=True,
                                   blank=True,
                                   verbose_name="描述")
    # 为了避免删除关联记录，bigang里所有外键都是on_delete=models.SET_NULL
    create_user = models.ForeignKey(User,
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    verbose_name="用户")
    # auto_now用于orm更新记录时，每次自动更新此字段时间
    update_date = models.DateTimeField(auto_now=True)
    # auto_now_add只用于第一次新增时，自动更新此字段时间
    create_date = models.DateTimeField(auto_now_add=True)
    # 用于扩展
    base_status = models.BooleanField(default=True)
    # django的simple_history库，加此字段，用于自动保存每个表的操作历史
    history = HistoricalRecords(inherit=True)

    # property用于为orm查询增加一个计算型字段
    @property
    def username(self):
        return self.create_user.username

    # 记录的默认显示值
    def __str__(self):
        return self.name

    class Meta:
        # abstract关键字，表示此class不会生成数据表，只能被继承使用
        abstract = True
        # 默认排序规则，按更新时间降序
        ordering = ('-update_date',)
