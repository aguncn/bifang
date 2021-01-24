import uuid
from django.contrib.auth import get_user_model
from cmdb.models import ReleaseStatus
from cmdb.models import Release
from cmdb.models import Env
from cmdb.models import Server
from cmdb.history_models import ReleaseHistory
from cmdb.history_models import ServerHistory

User = get_user_model()


def write_release_history(release_name=None, env_name=None, deploy_status_name=None,
                          deploy_type=None, log=None, user_id=None):
    name = uuid.uuid1()
    deploy_status = ReleaseStatus.objects.get(name=deploy_status_name)
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
                                  deploy_status=deploy_status,
                                  deploy_type=deploy_type,
                                  log=log,
                                  create_user=create_user)


def write_server_history():
    pass
