import gitlab
import time


def gitlab_trigger(git_url, git_access_token,
                   project_id, app_name, release,
                   git_branch, git_trigger_token,
                   build_script, deploy_script,
                   zip_package_name, file_up_server):
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
                                                   'ZIP_PACKAGE_NAME': zip_package_name,
                                                   'FILE_UP_SERVER': file_up_server})
    return pipeline


def pipeline_status(git_url, git_access_token, project_id, pipeline_id):
    git_url = git_url
    git_access_token = git_access_token
    gl = gitlab.Gitlab(git_url, private_token=git_access_token)

    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    time.sleep(1)
    pipeline.refresh()
    return pipeline

