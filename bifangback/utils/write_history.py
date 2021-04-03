import uuid
from django.contrib.auth import get_user_model
from cmdb.models import ReleaseStatus
from cmdb.models import ServerStatus
from cmdb.models import Release
from cmdb.models import App
from cmdb.models import Env
from cmdb.models import Server
from cmdb.history_models import ReleaseHistory
from cmdb.history_models import ServerHistory

User = get_user_model()


# 更新发布单状态
def update_release_status(release_name, app_name, env_name, deploy_no, release_status_name):
    if release_status_name != 'Check':
        # 如果是进行中或失败，直接写入
        release_status = ReleaseStatus.objects.get(name=release_status_name)
        release = Release.objects.filter(name=release_name).update(deploy_no=deploy_no, release_status=release_status)
    else:
        # 如果是只是完成其中一次的成功部署，Check时，则要判断同一个应用同一个环境的所有服务器的状态
        # 判断条件有两个：服务器上的主发布单与部署一致，所有服务器的部署状态为成功
        release = Release.objects.get(name=release_name)
        server_status = ServerStatus.objects.get(name='Success')
        release_status = ReleaseStatus.objects.get(name='Success')
        app = App.objects.get(name=app_name)
        env = Env.objects.get(name=env_name)
        servers = Server.objects.filter(app=app, env=env)
        for server in servers:
            if server.main_release != release or server.server_status != server_status:
                print("not meet")
                return
        print("all meet")
        release = Release.objects.filter(name=release_name).update(deploy_no=deploy_no,
                                                                   release_status=release_status)


# 更新服务器状态
def update_server_status(target_list, service_port, deploy_no, server_status_name):
    for ip in target_list:
        server_name = '{}_{}'.format(ip, service_port)
        server_status = ServerStatus.objects.get(name=server_status_name)
        server = Server.objects.filter(name=server_name).update(deploy_no=deploy_no, server_status=server_status)


# 更新服务器的主备发布单
def update_server_release(target_list, service_port, release_name, deploy_type):

    for ip in target_list:
        server = Server.objects.get(name='{}_{}'.format(ip, service_port))
        # 真正部署时，将服务器的主发布单放到备用发布单，用新发布单填充主发布单
        if deploy_type == 'deploy':
            release = Release.objects.get(name=release_name)
            # 如果存在部署，且不是重复部署
            if server.main_release and release != server.main_release:
                back_release = server.main_release
                server.back_release = back_release
            server.main_release = release
            server.save()

        # 如果是回滚，则将主备发布单都设置为备用发布单即可，因为只支持一次回滚。多次回滚，不如重新发布咯~~
        else:
            release = server.back_release
            server.main_release = release
            server.save()


# 更新发布单历史，这样可以串联起来发布单的操作历史，但操作服务器历史不在此之列，在下一个函数
def write_release_history(release_name=None, env_name=None,
                          release_status_name=None, deploy_type=None,
                          deploy_no=None, log=None, user_id=None):
    name = uuid.uuid1()
    release_status = ReleaseStatus.objects.get(name=release_status_name)
    release = Release.objects.get(name=release_name)
    create_user = None
    if user_id is not None:
        create_user = User.objects.get(id=user_id)
    env = None
    if env_name is not None:
        env = Env.objects.get(name=env_name)
    ReleaseHistory.objects.create(name=name,
                                  release=release,
                                  env=env,
                                  release_status=release_status,
                                  deploy_type=deploy_type,
                                  log_no=deploy_no,
                                  log=log,
                                  create_user=create_user)


# 更新服务器操作历史，可用ajax展示具体部署过程，也可以查看一个具体服务器的操作历史
def write_server_history(ip=None, service_port=None, release_name=None,
                         env_name=None, op_type=None,
                         action_type=None, deploy_no=None, log=None,
                         user_id=None):
    name = uuid.uuid1()
    server = Server.objects.get(name='{}_{}'.format(ip, service_port))
    release = None
    if release_name is not None:
        release = Release.objects.get(name=release_name)
    create_user = None
    if user_id is not None:
        create_user = User.objects.get(id=user_id)
    env = None
    if env_name is not None:
        env = Env.objects.get(name=env_name)
    ServerHistory.objects.create(name=name,
                                 release=release,
                                 env=env,
                                 server=server,
                                 op_type=op_type,
                                 action_type=action_type,
                                 log_no=deploy_no,
                                 log=log,
                                 create_user=create_user)
