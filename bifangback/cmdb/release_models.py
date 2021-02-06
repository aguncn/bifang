from django.db import models
from .base_models import BaseModel
from .app_models import App
from .env_models import Env


# 发布单状态，为了能动态管理，我觉得加个单独的表，有必要。
class ReleaseStatus(BaseModel):
    # ['Create', 'Building', 'BuildFailed', 'Build', 'Ready', 'Ongoing', 'Success', 'Failed']
    # ['创建', '编译中', '编译失败', '编译成功', '准备部署', '部署中', '部署成功', '部署失败']
    status_value = models.CharField(max_length=1024, blank=True, verbose_name="状态值")

    class Meta:
        db_table = 'ReleaseStatus'
        verbose_name = 'ReleaseStatus发布单状态'
        verbose_name_plural = 'ReleaseStatus发布单状态'


# 发布单， bifang部署平台中的灵魂和纽带
# 各种配置经由它作融合，各种动态数据经由它启动发散
class Release(BaseModel):
    # app关联
    app = models.ForeignKey(App,
                            related_name='ra_release',
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="应用")
    # 环境关联，这个在新建和编译发布单过程中，是没有数据的，在环境流转之后才有
    env = models.ForeignKey(Env,
                            related_name="ra_release",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="环境")
    # 如果一个发布单部署了多次，或是分批在服务器部署，就有这个记录的必要性了。
    deploy_no = models.IntegerField(blank=True,
                                    null=True,
                                    default=0,
                                    verbose_name="部署次数")
    # 自定义需要部署的git分支
    git_branch = models.CharField(max_length=255,
                                  blank=True,
                                  null=True)
    # pipeline_id和pipeline_url在编译软件包的过程中生成，用于获取编译状态及定位编译输出
    pipeline_id = models.IntegerField(default=0)
    pipeline_url = models.URLField(default='http://www.demo.com')
    # 这个部署脚本，在git代码中的一般会有自己独立的目录，而在制品仓库时，可能就有软件包并列在同一个目录了，清晰。
    deploy_script_url = models.URLField(default=None,
                                        blank=True,
                                        null=True,
                                        verbose_name="部署脚本路径")
    # 这里生成软件包之后，直接记录url软件包路径，这样在部署脚本中，就可以直接使用wget下载了。
    # 为什么不使用salt？其实也行，但wget不是更稳定和简单么？
    zip_package_url = models.URLField(default=None,
                                      blank=True,
                                      null=True,
                                      verbose_name="压缩制品库路径")
    # 记录各种状态用于前端显示
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
