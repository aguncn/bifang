from django.core.management.base import BaseCommand, CommandError
from cmdb.models import *
from datetime import datetime
from django.utils import timezone
import pytz
import random
from django.core.management.base import BaseCommand, CommandError
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
                             git_url='http://192.168.1.211:8090/',
                             git_user='git_user',
                             git_pwd='git_pwd')
        self.stdout.write('GitTb重建完成。')

    # 新建一个SaltApi
    def add_salt(self):
        SaltTb.objects.all().delete()
        create_user = User.objects.get(username=username)
        SaltTb.objects.create(name='MainSalt',
                              description='主要SaltApi',
                              create_user=create_user,
                              salt_url='http://192.168.1.211:8080/',
                              salt_user='git_user',
                              salt_pwd='git_pwd')
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
