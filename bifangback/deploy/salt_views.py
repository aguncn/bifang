from saltypie import Salt
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bifangback.settings")
django.setup()

from django.conf import settings
from cmdb.models import App
from cmdb.models import Env
from cmdb.models import Release
from utils.saltstack import salt_cmd

env = Env.objects.get(name='dev')
app = App.objects.get(name='go-demo')
release = Release.objects.get(name='20210116131554484444EJ')

salt_url = env.salt.salt_url
salt_user = env.salt.salt_user
salt_pwd = env.salt.salt_pwd
eauth = env.salt.eauth
target_list = ['192.168.1.211']

app_name = app.name
release_name = release.name
deploy_script_url = release.deploy_script_url
zip_package_name = app.zip_package_name
zip_package_url = release.zip_package_url
service_port = app.service_port

action = 'health_check'

ret = salt_cmd(salt_url, salt_user, salt_pwd, eauth,
               target_list, deploy_script_url,
               app_name, release, env, action,
               zip_package_name, zip_package_url,
               service_port)
for server in ret:
    for ip, detail in server.items():
        print('ip: ', ip)
        print('retcode: ', detail['retcode'])
        print('stdout: ', detail['stdout'])
        print('stderr: ', detail['stderr'])
        print('pid: ', detail['pid'])



