from django.db import models
from .base_models import BaseModel
from .git_models import GitTb
from .project_models import Project


# 应用服务，相当于一个可独立部署的微服务
# 如istio bookinfo中，可独立部署，且使用不同语言开发的4个应用(productpage, details, reviews, ratings)
class App(BaseModel):
    # cn_name和app_id意义和project中的一样。但要注意，这个app_id，会和一些外键表中的app_id有雷同，这是高级技巧了，
    # 这是一个坑，但本来这样命名，也是最自然的，无所畏惧。
    cn_name = models.CharField(max_length=255, verbose_name="中文名")
    app_id = models.IntegerField(default=0, verbose_name="应用编号")
    # 每个app应用，与一个代码关联
    git = models.ForeignKey(GitTb,
                            related_name="ra_app",
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name="Git实例")
    # 这里单独定义一个git中这个app的id，可能有优化的空间，也可能没有。git库在定义具体的代码仓库时，就是要这个参数
    git_app_id = models.IntegerField(default=0, verbose_name="Git应用ID")
    # 为了加强控制，git中每一个ci/cd功能，当代码提交之后，都不会自动运行，而要通过一个trigger token去人工触发
    # 这个trigger token的生成，在gitlab的ci/cd里，很容易生成。
    git_trigger_token = models.CharField(max_length=64,
                                         blank=True,
                                         null=True,
                                         verbose_name="git trigger token")
    # 将app与project进行关联，方便数据统计，关联显示
    project = models.ForeignKey(Project,
                                related_name='ra_project',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='项目')
    # 按devops及gitops的理念，开发维护自己的编译脚本和部署脚本，并进行版本管理
    # build_script用于定义通过构建，生成软件包的脚本
    build_script = models.CharField(max_length=255, default='build.sh', verbose_name="编译脚本名")
    # deploy_script用于定义服务部署，启停，备份，回滚，健康状态检测等功能，
    # 如果为开发提供了模板，是很容易作为代码一部份管理起来的，配置即代码！
    # 如果bifang本身来存储这些脚本，反而增加管理难度，不透明度及中心化
    deploy_script = models.CharField(max_length=255, default='bifang.sh', verbose_name="部署脚本名")
    # 定义软件包的名称，这里也有纠结，是自定义，还是强约定
    # 如果规定了软件包名必须与app名称相同，会少很多事，但又显得过于霸道
    # 这里留个小口吧，另外，在部署脚本时，还会有几个类似的软件包，软件压缩包名，软件部署目录，都类似
    zip_package_name = models.CharField(max_length=255, default='demo.zio', verbose_name="应用压缩包")
    # 如果app有脚本端口，则可能用于状态检测，增加部署的成功判断率
    service_port = models.IntegerField(default=0, verbose_name="服务端口")
    # 使用哪个用户名和哪个用户组启动，
    service_username = models.CharField(max_length=24,
                                        blank=True,
                                        null=True,
                                        verbose_name="执行用户名")
    service_group = models.CharField(max_length=24,
                                     blank=True,
                                     null=True,
                                     verbose_name="执行用户组")
    # 如果bifang增加独立的服务器启停功能，日志单独数据表保存，但这里可以保存最近启停次数，用于定义日志
    op_log_no = models.IntegerField(default=0, verbose_name="启停日志次数")

    class Meta:
        db_table = 'App'
        verbose_name = 'App应用'
        verbose_name_plural = 'App应用'
