from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="名称")
    description = models.CharField(max_length=100,
                                   null=True,
                                   blank=True,
                                   verbose_name="描述")
    create_user = models.ForeignKey(User,
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    verbose_name="用户")
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    base_status = models.BooleanField(default=True)
    history = HistoricalRecords(inherit=True)

    @property
    def username(self):
        return self.create_user.username

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('-update_date',)
