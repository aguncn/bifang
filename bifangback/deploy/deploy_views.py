import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from asgiref.sync import async_to_sync
from cmdb.models import App
from utils.saltstack import salt_cmd
from cmdb.models import Env
from cmdb.models import Release
from .serializers import DeploySerializer
from utils.ret_code import *


@async_to_sync
# django异步视图
async def deploy(request):
    if request.method == 'POST':
        """
        {
            "app_name": "go-demo",
            "env_name":"dev",
            "release_name": "20210117132941344089GA",
            "deploy_type": "deploy",
            "op_type": "deploy",
            "target_list": ["192.168.1.211", "192.168.1.212"]
        }
        """
        req_data = json.loads(request.body.decode('utf-8'))
        # 序列化前端数据，并判断是否有效
        serializer = DeploySerializer(data=req_data)
        if serializer.is_valid():
            ser_data = serializer.validated_data
            app_name = ser_data['app_name']
            release_name = ser_data['release_name']
            env_name = ser_data['env_name']
            # op_type用于定义是部署应用，还是服务器启停，deploy_type用于定义操作指令
            op_type = ser_data['op_type']
            deploy_type = ser_data['deploy_type']
            target_list = ser_data['target_list']

            if deploy_type == 'deploy' and op_type == 'deploy':
                action_list = ['fetch', 'stop', 'stop_status', 'deploy', 'start', 'start_status', 'health_check']
            elif deploy_type == 'rollback' and op_type == 'deploy':
                action_list = ['stop', 'stop_status', 'rollback', 'start', 'start_status', 'health_check']
            elif deploy_type == 'stop' and op_type == 'maintenance':
                action_list = ['stop', 'stop_status']
            elif deploy_type == 'start' and op_type == 'maintenance':
                action_list = ['start', 'start_status']
            elif deploy_type == 'restart' and op_type == 'maintenance':
                action_list = ['stop', 'stop_status', 'start', 'start_status']
            else:
                pass

            loop = asyncio.get_event_loop()
            loop.create_task(thread_async(action_list, env_name, app_name, release_name, target_list))

            return_dict = build_ret_data(OP_SUCCESS, 'success')
            return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)


# 异步任务
async def thread_async(action_list, env_name, app_name, release_name, target_list):

    try:
        await asyncio.sleep(1)
        for action in action_list:
            print('action: ', action)
            # 多线程版本，应用为IO密集型，适合threading模式
            executor = ThreadPoolExecutor()
            for data in executor.map(cmd_run, [env_name], [app_name], [release_name], [target_list], [action]):
                if not data:
                    print('data_false: ', data)
                    return_dict = build_ret_data(THROW_EXP, action)
                    return render_json(return_dict)
                print('data_true: ', data)
        print("finish: ", action_list, env_name, app_name, release_name, target_list)
    except asyncio.CancelledError:
        print('Cancel the future.')
    except Exception as e:
        print(e)


# cmd_run函数是在每一个线程当中运行的
def cmd_run(env_name, app_name, release_name, target_list, action):
    print(env_name, app_name, release_name, target_list, action, "@@@@@@@@@")
    env = Env.objects.get(name=env_name)
    app = App.objects.get(name=app_name)
    release = Release.objects.get(name=release_name)

    salt_url = env.salt.salt_url
    salt_user = env.salt.salt_user
    salt_pwd = env.salt.salt_pwd
    eauth = env.salt.eauth

    deploy_script_url = release.deploy_script_url
    zip_package_name = app.zip_package_name
    zip_package_url = release.zip_package_url
    service_port = app.service_port

    ret = salt_cmd(salt_url, salt_user, salt_pwd, eauth,
                   target_list, deploy_script_url,
                   app_name, release, env, action,
                   zip_package_name, zip_package_url,
                   service_port)
    time.sleep(1)
    for server in ret:
        for ip, detail in server.items():
            print('ip: ', ip)
            print('retcode: ', detail['retcode'])
            print('stdout: ', detail['stdout'])
            print('stderr: ', detail['stderr'])
            print('pid: ', detail['pid'])
    return True
