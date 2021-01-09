import gitlab
import time

git_url = 'http://192.168.1.211:8180'
git_access_token = 'RbCcuLssPekyVgy24Nui'
gl = gitlab.Gitlab(git_url, private_token=git_access_token)

project_id = 1
project = gl.projects.get(project_id)

app_name = 'go-demo'
release = '202101090345XF'

pipeline = project.trigger_pipeline('master',
                                    '559fbd3381bc39100811bd00e499a7',
                                    variables={"RELEASE": release,
                                               'APP_NAME': app_name})
while pipeline.finished_at is None:
    pipeline.refresh()
    print(pipeline)
    time.sleep(1)
