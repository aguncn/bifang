from saltypie import Salt


def salt_cmd(salt_url, salt_user, salt_pwd, eauth,
             target_list, script_url,
             app, release, env,
             zip_package_name, zip_package_url,
             service_port, action):

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
    # print(arg_list)
    exe_return = salt.execute(
        client=Salt.CLIENT_LOCAL,
        target=target_list,
        tgt_type='list',
        fun='cmd.script',
        args=arg_list,
    )
    # print(exe_return)
    return exe_return['return']