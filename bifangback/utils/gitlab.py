import gitlab
import time


def gitlab_trigger(git_url, git_access_token,
                   project_id, app_name, release,
                   git_branch, git_trigger_token,
                   build_script, deploy_script, file_up_server):
    git_url = git_url
    git_access_token = git_access_token
    gl = gitlab.Gitlab(git_url, private_token=git_access_token)

    project = gl.projects.get(project_id)

    pipeline = project.trigger_pipeline(git_branch,
                                        git_trigger_token,
                                        variables={"RELEASE": release,
                                                   'APP_NAME': app_name,
                                                   'BUILD_SCRIPT': build_script,
                                                   'DEPLOY_SCRIPT': deploy_script,
                                                   'FILE_UP_SERVER': file_up_server})
    while pipeline.finished_at is None:
        pipeline.refresh()
        time.sleep(1)
    return pipeline

