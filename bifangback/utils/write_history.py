import uuid
from cmdb.history_models import ReleaseHistory
from cmdb.history_models import ServerHistory


def write_release_history(release=None, env=None, deploy_status=None,
                          deploy_type=None, log=None, create_user=None):
    name = uuid.uuid1()
    ReleaseHistory.objects.create(name=name,
                          release=release,
                          env=env,
                          deploy_status=deploy_status,
                          deploy_type=deploy_type,
                          log=log,
                          create_user=create_user)


def write_server_history():
    pass
