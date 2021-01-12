from saltypie import Salt
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bifangback.settings")
django.setup()

from django.conf import settings
from cmdb.models import App
from cmdb.models import Env
from utils.saltstack import salt_cmd

env = Env.objects.get(name='dev')
app = App.objects.get(name='go-demo')

salt_url = env.salt.salt_url
salt_user = env.salt.salt_user
salt_pwd = env.salt.salt_pwd
eauth = env.salt.eauth
target_list = ['192.168.1.211']

app_name = app.name
release = '202101090245XX'
deploy_script = app.deploy_script
# 部署脚本在上传时，只取了最后的文件名，目录名被忽略，这里也要作转换
script = os.path.basename(deploy_script)
script_url = '{}/{}/{}/{}'.format(settings.FILE_DOWN_SERVER, app_name, release, script)
cmd = 'status'

ret = salt_cmd(salt_url, salt_user, salt_pwd, eauth,
               target_list, script_url, release, env, cmd)
for server in ret:
    for ip, detail in server.items():
        print(ip, detail['retcode'], detail['stdout'], detail['stderr'], detail['pid'])



