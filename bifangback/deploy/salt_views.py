from saltypie import Salt

salt = Salt(
    url='https://192.168.1.211:8000',
    username='saltapi',
    passwd='saltapipwd',
    trust_host=True,
    eauth='pam'
)

arg_list = [
    'http://192.168.1.111:9002/go-demo/202101090345XF/bifang.sh',
    '202101090345XF dev status',
]
tgt_list = ['192.168.1.211', '192.168.1.212']

exe_return = salt.execute(
    client=Salt.CLIENT_LOCAL,
    target=tgt_list,
    tgt_type='list',
    fun='cmd.script',
    args=arg_list,
)

print(exe_return['return'])

