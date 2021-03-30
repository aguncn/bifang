from saltypie import Salt

salt_url = 'https://192.168.1.211:8000'
salt_user = 'saltapi'
salt_pwd = 'saltapipwd'
eauth = 'pam'
target_list = ['192.168.1.212']
script_url = 'http://192.168.1.211:9002/go-demo/20210320104629503523FC/deploy.sh'
app = 'go-demo'
release = '20210320104629503523FC'
env = 'dev'
zip_package_name = 'go-demo.tar.gz'
zip_package_url = 'http://192.168.1.211:9002/go-demo/20210320104629503523FC/go-demo.tar.gz'
service_port = '9090'
# 更改此处即可测试不同的action
action = 'start'


def salt_cmd():

    salt = Salt(
        url=salt_url,
        username=salt_user,
        passwd=salt_pwd,
        trust_host=True,
        eauth=eauth
    )

    arg_list = [script_url, '{} {} {} {} {} {} {}'.format(app, release, env,
                                                          zip_package_name, zip_package_url,
                                                          service_port, action)]
    exe_return = salt.execute(
        client=Salt.CLIENT_LOCAL,
        target=target_list,
        tgt_type='list',
        fun='cmd.script',
        args=arg_list,
    )
    return exe_return['return']


# 使用saltypie来获取返回值，不自己写Http请求，更容易解析结果
ret = salt_cmd()
# salt找不到服务器，则返回列表里字典中有一个必为空，这一步要提前判断
if any(not item for item in ret):
    print('找不到salt minion客户端：' + str(ret))
for server in ret:
    for ip, detail in server.items():
        print('ip: ', ip)
        print('retcode: ', detail['retcode'])
        print('stdout: ', detail['stdout'])
        print('stderr: ', detail['stderr'])
        print('pid: ', detail['pid'])