import time
from django.contrib.auth import get_user_model
from cmdb.models import App
from utils.saltstack import salt_cmd
from cmdb.models import Env
from cmdb.models import Release
from .serializers import DeploySerializer
from utils.ret_code import *
from utils.permission import is_right
from utils.write_history import update_release_status
from utils.write_history import write_release_history
from utils.write_history import write_server_history
from utils.write_history import update_server_release

User = get_user_model()


def deploy(request):
    if request.method == 'POST':
        """
        {
            "app_name": "go-demo",
            "env_name":"dev",
            "user_id":111,
            "release_name": "20210117132941344089GA",
            "deploy_type": "deploy",
            "deploy_no": 1,
            "op_type": "deploy",
            "target_list": ["192.168.1.211", "192.168.1.212"]
        }
        """
        req_data = json.loads(request.body.decode('utf-8'))
        req_data['target_list'] = req_data['target_list'].split(',')
        # 序列化前端数据，并判断是否有效
        serializer = DeploySerializer(data=req_data)
        if serializer.is_valid():
            ser_data = serializer.validated_data
            app_name = ser_data['app_name']
            service_port = ser_data['service_port']
            release_name = ser_data['release_name']
            env_name = ser_data['env_name']
            user_id = ser_data['user_id']
            # op_type用于定义是部署应用，还是服务器启停，deploy_type用于定义操作指令
            op_type = ser_data['op_type']
            deploy_type = ser_data['deploy_type']
            target_list = ser_data['target_list']
            # 部署批次是在当前发布单的部署批次上加1，然后，将这个批次分别传到部署历史和服务器历史中，以对应日志
            deploy_no = int(ser_data['deploy_no']) + 1
            """
            # 前端开发完成后开启权限测试
            app = App.objects.get(name=app_name)
            user = request.user
            action = Action.objects.get(name='Deploy')
            if not is_right(app.id, action.id, user):
                return_dict = build_ret_data(THROW_EXP, '你无权限部署此应用！')
                return render_json(return_dict)
            """
            # op_type的deploy用来部署发布音，maintenance用来启停服务
            if deploy_type == 'deploy' and op_type == 'deploy':
                action_list = ['fetch', 'stop', 'stop_status', 'deploy', 'start', 'start_status', 'health_check']
                # 更新发布单历史及状态
                write_release_history(release_name, env_name, 'Ongoing', deploy_type, deploy_no, 'Ongoing', user_id)
                update_release_status(release_name, deploy_no, 'Ongoing')
            # 回滚，只更新服务器操作历史及服务器主备发布单
            elif deploy_type == 'rollback' and op_type == 'deploy':
                action_list = ['stop', 'stop_status', 'rollback', 'start', 'start_status', 'health_check']
            # 之后的代码判断逻辑，可以用来处理单纯的服务器应用启停，而不需要部署发布单
            elif deploy_type == 'stop' and op_type == 'maintenance':
                action_list = ['stop', 'stop_status']
            elif deploy_type == 'start' and op_type == 'maintenance':
                action_list = ['start', 'start_status']
            elif deploy_type == 'restart' and op_type == 'maintenance':
                action_list = ['stop', 'stop_status', 'start', 'start_status']
            else:
                return_dict = build_ret_data(THROW_EXP, '异常流程参数')
                return render_json(return_dict)

            task_run(action_list, env_name,
                     app_name, service_port, release_name,
                     target_list, user_id,
                     op_type, deploy_type, deploy_no)

            return_dict = build_ret_data(OP_SUCCESS, 'success')
            return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)


def task_run(action_list, env_name,
             app_name, service_port, release_name,
             target_list, user_id,
             op_type, deploy_type, deploy_no):

    try:
        for action in action_list:
            print('action: ', action)

            ret_data = cmd_run(env_name, app_name,
                               service_port, release_name,
                               target_list, action,
                               user_id, op_type, deploy_type, deploy_no)
            if not ret_data:
                # print('data_false: ', data)
                # 有真正部署，出错时才需要更新发布单历史，其它情况，只更新服务器发布历史(暂不考虑回滚失败)
                if deploy_type == 'deploy':
                    write_release_history(release_name, env_name, 'Failed', deploy_type, deploy_no, 'Failed', user_id)
                    update_release_status(release_name, deploy_no, 'Failed')
                return_dict = build_ret_data(THROW_EXP, action)
                return render_json(return_dict)
            # print('data_true: ', data)
        # 只有部署和回滚，才需要更新发布单历史和服务器主备发布单(回滚时，发布单参数并没有用上)
        if op_type == 'deploy':
            write_release_history(release_name, env_name, 'Success', deploy_type, deploy_no, 'Success', user_id)
            update_server_release(target_list, service_port, release_name, deploy_type)
            update_release_status(release_name, deploy_no, 'Success')
        print("finish: ", action_list, env_name, app_name, release_name, target_list)
    except Exception as e:
        print(e)


# cmd_run函数是在每一个线程当中运行的
def cmd_run(env_name, app_name, service_port,
            release_name, target_list,
            action, user_id,
            op_type, deploy_type, deploy_no):
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
    # 使用saltypie来获取返回值，不自己更写Http请求，更容易解析结果
    ret = salt_cmd(salt_url, salt_user, salt_pwd, eauth,
                   target_list, deploy_script_url,
                   app_name, release, env,
                   zip_package_name, zip_package_url,
                   service_port, action)
    time.sleep(1)
    # salt找不到服务器，则返回列表里字典中有一个必为空，这一步要提前判断
    if any(not item for item in ret):
        return False
    for server in ret:
        for ip, detail in server.items():
            # 记录服务器操作历史
            write_server_history(ip, service_port, release_name, env_name, op_type, action, deploy_no, detail['stdout'], user_id)
            # 部署脚本的每一个步骤，成功时必须返回success关键字
            if 'success' not in detail['stdout']:
                return False
            """
            print('ip: ', ip)
            print('retcode: ', detail['retcode'])
            print('stdout: ', detail['stdout'])
            print('stderr: ', detail['stderr'])
            print('pid: ', detail['pid'])
            """
    return True
