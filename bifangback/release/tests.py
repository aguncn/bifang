import gitlab

git_url = 'http://192.168.1.211:8180'
git_access_token = 'yixczsJ6xupwpKZNvRgj'
project_id = 1
app_name = 'go-demo'
release_name = '2021-04-01'
git_branch = 'master'
git_trigger_token = '559fbd3381bc39100811bd00e499a7'
build_script = 'script/build.sh'
deploy_script = 'script/deploy.sh'
zip_package_name = 'go-demo.tar.gz'
file_up_server = 'http://192.168.1.211:9001/upload-file'


def main():
    try:
        gl = gitlab.Gitlab(git_url, private_token=git_access_token)
        project = gl.projects.get(project_id)
        pipeline = project.trigger_pipeline(git_branch,
                                            git_trigger_token,
                                            variables={"RELEASE": release_name,
                                                       'APP_NAME': app_name,
                                                       'BUILD_SCRIPT': build_script,
                                                       'DEPLOY_SCRIPT': deploy_script,
                                                       'ZIP_PACKAGE_NAME': zip_package_name,
                                                       'FILE_UP_SERVER': file_up_server})
        print(pipeline.id)
        print(pipeline.web_url)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

