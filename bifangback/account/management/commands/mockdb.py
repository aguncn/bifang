from django.core.management.base import BaseCommand, CommandError
from cmdb.models import *
import string
import random
import time
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'


# 自定义命令，用于建立测试数据，很多ORM语句会使用
class Command(BaseCommand):
    help = 'create test data for BiFang back server.'

    def add_arguments(self, parser):
        self.stdout.write(self.style.SUCCESS('没有额外参数，新建全部模拟测试数据，删除所有旧记录'))

    def handle(self, *args, **options):
        self.add_user()
        self.add_git()
        self.add_salt()
        self.add_env()
        self.add_project()
        self.add_app()
        self.add_server()
        self.add_release_status()
        self.add_release()
        self.add_action()
        self.add_permission()
        self.stdout.write(self.style.SUCCESS('数据重建完成，一把梭哈~~~'))
        # raise CommandError('Ok！')

    # 新建一个用户
    def add_user(self):
        User.objects.all().delete()
        User.objects.create_user(username=username,
                                 password='password',
                                 is_staff=True,
                                 is_active=True,
                                 is_superuser=True)
        self.stdout.write('用户{}重建完成。'.format(username))

    # 新建一个Git仓库
    def add_git(self):
        GitTb.objects.all().delete()
        create_user = User.objects.get(username=username)
        GitTb.objects.create(name='MainGit',
                             description='主要git库',
                             create_user=create_user,
                             git_url='http://192.168.1.211:8180',
                             git_token='RbCcuLssPekyVgy24Nui')
        self.stdout.write('GitTb重建完成。')

    # 新建一个SaltApi
    def add_salt(self):
        SaltTb.objects.all().delete()
        create_user = User.objects.get(username=username)
        SaltTb.objects.create(name='MainSalt',
                              description='主要SaltApi',
                              create_user=create_user,
                              salt_url='https://192.168.1.211:8000',
                              salt_user='saltapi',
                              salt_pwd='saltapipwd',
                              eauth='pam',
                              trust_host=True)
        self.stdout.write('SaltTb重建完成。')

    # 新建一个环境
    def add_env(self):
        Env.objects.all().delete()
        create_user = User.objects.get(username=username)
        salt = SaltTb.objects.order_by('?').first()
        env_list = ['dev', 'prd']
        for index, env in enumerate(env_list):
            Env.objects.create(name=env,
                               description=env,
                               create_user=create_user,
                               env_id=index,
                               salt=salt)
        self.stdout.write('Env重建完成。')

    # 新建demo项目
    def add_project(self):
        Project.objects.all().delete()
        create_user = User.objects.get(username=username)
        project_name_list = ['User', 'Service', 'Store', 'Card', 'Support']
        project_cn_name_list = ['用户管理', '服务', '库存', '购物车', '客服']
        for project_name, project_cn_name in zip(project_name_list, project_cn_name_list):
            Project.objects.create(name=project_name,
                                   description=project_name,
                                   cn_name=project_cn_name,
                                   create_user=create_user,
                                   project_id=random.randint(1000, 10000))
        self.stdout.write('Project重建完成。')

    # 新建demo应用
    def add_app(self):
        App.objects.all().delete()
        create_user = User.objects.get(username=username)
        app_name_list = ['User-Login', 'Service-724', 'Store-Address', 'Card-Adjust', 'Support-Admin', 'go-demo']
        app_cn_name_list = ['用户登陆', '全天服务', '库存地址', '购物车调配', '客服后管', '毕方演示go示例']
        for app_name, app_cn_name in zip(app_name_list, app_cn_name_list):
            git = GitTb.objects.order_by('?').first()
            project = Project.objects.order_by('?').first()
            App.objects.create(name=app_name,
                               description=app_name,
                               cn_name=app_cn_name,
                               create_user=create_user,
                               app_id=random.randint(10000, 100000),
                               git=git,
                               git_app_id=1,
                               git_trigger_token='559fbd3381bc39100811bd00e499a7',
                               project=project,
                               build_script='script/build.sh',
                               deploy_script='script/bifang.sh',
                               zip_package_name='go-demo.tar.gz',
                               service_port=9090,
                               service_username='sky',
                               service_group='operate')
        self.stdout.write('App重建完成。')

    # 新建server服务器
    def add_server(self):
        Server.objects.all().delete()
        create_user = User.objects.get(username=username)
        for number in range(100):
            ip = '192.168.1.{}'.format(number)
            app = App.objects.order_by('?').first()
            Server.objects.create(name=ip,
                                  description=ip,
                                  create_user=create_user,
                                  ip=ip,
                                  port=random.randint(10000, 100000),
                                  app=app,
                                  system_type=random.choice(['WINDOWS', 'LINUX']))
        self.stdout.write('Server重建完成。')

    # 新建发布单状态
    def add_release_status(self):
        ReleaseStatus.objects.all().delete()
        create_user = User.objects.get(username=username)
        status_list = ['Create', 'Building', 'Build', 'Ready', 'Ongoing', 'Success', 'Failed']
        status_value_list = ['创建', '编译', '就绪', '部署中', '成功', '失败']
        for status_name, status_value_name in zip(status_list, status_value_list):
            ReleaseStatus.objects.create(name=status_name,
                                         description=status_name,
                                         create_user=create_user,
                                         status_value=status_value_name)
        self.stdout.write('ReleaseStatus重建完成。')

    # 新建demo发布单
    def add_release(self):
        Release.objects.all().delete()
        create_user = User.objects.get(username=username)
        for number in range(100):
            app = App.objects.order_by('?').first()
            env = Env.objects.order_by('?').first()
            deploy_status = ReleaseStatus.objects.order_by('?').first()
            random_letter = ''.join(random.sample(string.ascii_letters, 2))

            name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + random_letter.upper()
            Release.objects.create(name=name,
                                   description=name,
                                   create_user=create_user,
                                   app=app,
                                   env=env,
                                   git_branch='master',
                                   pipeline_id=0,
                                   pipeline_url='http://www.demo.com',
                                   deploy_script_url='http://192.168.1.213:8080/a/b/bifang.sh',
                                   zip_package_url='http://192.168.1.213:8080/a/b/go-demo.zip',
                                   deploy_status=deploy_status)
        self.stdout.write('Release重建完成。')

    # 新建权限
    def add_action(self):
        Action.objects.all().delete()
        create_user = User.objects.get(username=username)
        Action.objects.create(name='Create',
                              description='创建编译权限',
                              create_user=create_user,
                              action_id=100)
        Action.objects.create(name='Deploy',
                              description='环境部署权限',
                              create_user=create_user,
                              action_id=1000)
        self.stdout.write('Action重建完成。')

    # 新建demo应用权限用户表
    def add_permission(self):
        Permission.objects.all().delete()
        create_user = User.objects.get(username=username)
        for number in range(2):
            app = App.objects.order_by('?').first()
            action = Action.objects.order_by('?').first()
            pm_user = User.objects.order_by('?').first()
            name = '{}-{}-{}'.format(app.name, action.name, pm_user.username)
            Permission.objects.create(name=name,
                                      description=name,
                                      create_user=create_user,
                                      app=app,
                                      action=action,
                                      pm_user=pm_user)
        self.stdout.write('Permission重建完成。')
