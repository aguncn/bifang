from django.db import models
from .base_models import BaseModel
from .app_models import App
from .release_models import Release
from .env_models import Env

SYSTEM_CHOICES = (
    ('WINDOWS', 'WINDOWS'),
    ('LINUX', 'LINUX'),
)


# 服务器状态，为了能动态管理，我觉得加个单独的表，有必要。
class ServerStatus(BaseModel):
    # ['Ready', 'Ongoing', 'Success', 'Failed']
    # ['准备部署', '部署中', '部署成功', '部署失败']
    status_value = models.CharField(max_length=1024, blank=True, verbose_name="状态值", default="Ready")

    class Meta:
        db_table = 'ServerStatus'
        verbose_name = 'ServerStatus服务器状态'
        verbose_name_plural = 'ServerStatus服务器状态'


# 为外键设置默认值
def get_server_status():
    return ServerStatus.objects.get_or_create(name='Ready')[0].id


# 部署服务器，保证ip和port结合起来的唯一性，可以一个服务器上部署多个应用
# （但不可以在同一个服务器的不同端口部署同一个应用，想想salt在执行同一批次执行到同一个服务器上的情况，会执行多次，也可以只一次详细考察target_list同为一个机器的情况吧）
# 当然，能在同一个服务器上，部署多个相同的应用，这得益于将部署脚本让开发自己维护。
# 真正的devops团队，是需要都有开发和运维的跨界实力的啦~
class Server(BaseModel):
    # GenericIPAddressField的字段，让这里只存储ip地址
    ip = models.GenericIPAddressField(max_length=64, verbose_name="服务器Ip")
    # 服务端口，其实，这里是需要优化的，
    # 如果有的服务启动，不提供端口服务呢？乱写么？如何保证多个无端口服务不冲突？
    port = models.IntegerField(verbose_name="服务器端口")
    system_type = models.CharField(max_length=16,
                                   choices=SYSTEM_CHOICES,
                                   default='LINUX',
                                   verbose_name="操作系统")
    # 此服务器与哪一个app关联
    app = models.ForeignKey(App,
                            related_name='ra_server',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name='应用服务')
    # 环境关联，在部署时，根据环境关联服务器
    env = models.ForeignKey(Env,
                            related_name="ra_server",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    # 保存在此服务器正在运行的app的最近发布单
    main_release = models.ForeignKey(Release,
                                     related_name='ra_server_main',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='主发布单')
    # 保存在此服务器正在运行的app的次新发布单，主要用于回滚，bifang只支持最近一次回滚，不支持无限回滚
    back_release = models.ForeignKey(Release,
                                     related_name='ra_server_back',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     verbose_name='备份发布单')
    # 如果一个发布单部署了多次，或是分批在服务器部署，就有这个记录的必要性了。用于判断服务器部署是否完成
    deploy_no = models.IntegerField(blank=True,
                                    null=True,
                                    default=0,
                                    verbose_name="部署次数")
    # 记录各种状态用于前端显示
    # 或发布进行中或完成的判断(主发布单和是否完成部署)
    server_status = models.ForeignKey(ServerStatus,
                                      related_name='ra_server',
                                      # default=get_server_status,
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name="服务器状态")

    class Meta:
        db_table = 'Server'
        # 一个服务器上，部署多个应用，保证Ip加port的唯一性。
        unique_together = ('ip', 'port')
        verbose_name = 'Server服务器'
        verbose_name_plural = 'Server服务器'
