#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import subprocess
import shutil
import time
import logging

# ###########从命令行获取的参数#################
# app名称
app_name = sys.argv[1]
# release发布单参数
release_name = sys.argv[2]
# env环境参数
env_name = sys.argv[3]
# app压缩包名参数
zip_package_name = sys.argv[4]
# app压缩包的网络下载地址
zip_package_url = sys.argv[5]
# port服务端口参数
port = sys.argv[6]
# action服务启停及部署参数
action = sys.argv[7]

# ###########自定义部署变量#################
# app可执行文件名或包名
PACKAGE_NAME = "go-demo"
# app部署根目录
APP_ROOT_HOME = './app'
# 可执行文件所有目录
BIN_PATH = './bin'
# app软件包保存根目录
LOCAL_ROOT_STORE = './var/ops'

# ###########部署路径#################
app_home = '{}/{}'.format(APP_ROOT_HOME, app_name)
local_store = '{}/{}/current'.format(LOCAL_ROOT_STORE, app_name)
local_back = '{}/{}/backup'.format(LOCAL_ROOT_STORE, app_name)
log_file = 'deploy.log'


class Deploy:
    def __init__(self):
        print('__init__')

    def shell(self, cmd):
        _status, _output = subprocess.getstatusoutput(cmd)
        self.logging(_output)
        if _status == 0:
            return _output
        else:
            print('{} command is execute wrongly.'.format(cmd))
            print(_output)
            sys.exit(1)

    def logging(self, log):
        logger = logging.getLogger()
        fh = logging.FileHandler(log_file, encoding="utf-8", mode="a")
        formatter = logging.Formatter("%(asctime)s - %(name)s-%(levelname)s %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.setLevel(logging.DEBUG)
        logger.debug(log)

    def make_dirs(self):
        if not os.path.exists(app_home):
            self.shell('mkdir -p {}'.format(app_home))
        if not os.path.exists(local_store):
            self.shell('mkdir -p {}'.format(local_store))
        if not os.path.exists(local_back):
            self.shell('mkdir -p {}'.format(local_back))

    def get_app_id(self):
        return self.shell("pgrep -f '{}'|grep -v 'salt'|grep -v 'grep'".format(PACKAGE_NAME))

    def fetch(self):
        self.make_dirs()
        # 删除上上次备份的软件包(无多次回滚)
        old_back_path = '{}/{}'.format(local_back, zip_package_name)
        if os.path.exists(old_back_path):
            self.shell('mv {} /tmp/'.format(old_back_path))
        # 备份上次的软件包
        current_back_path = '{}/{}'.format(local_store, zip_package_name)
        if os.path.exists(current_back_path):
            self.shell('mv {} {}'.format(current_back_path, old_back_path))

        # 获取本次的部署包
        self.shell('wget -q -P {} {}'.format(local_store, zip_package_url))
        print("APP_NAME: {} fetch zip package success.".format(app_name))

    def deploy(self):
        # 部署，从CURRENT目录解压恢复
        if not os.path.exists(app_home):
            shutil.move(app_home, '/tmp/')
        current_back_path = '{}/{}'.format(local_store, zip_package_name)
        self.shell('tar -xzvf  {} -C {} '.format(current_back_path, app_home))
        print("APP_NAME: {} deploy success.".format(app_name))

    def rollback(self):
        # 回滚，从BACKUP目录解压恢复
        old_back_path = '{}/{}'.format(local_back, zip_package_name)
        self.shell('mv {}/* /tmp/'.format(app_home))
        self.shell('tar -xzvf  {} -C {} '.format(old_back_path, app_home))
        print("APP_NAME: {} rollback success.".format(app_name))

    def start(self):
        if self.get_app_id():
            print("APP_NAME: {}  is running, kill first or restart, failure start.".format(app_name))
            sys.exit(1)
        # 此处为真正启动命令
        self.shell('nohup {}/{} >/dev/null 2>&1 &'.format(BIN_PATH, PACKAGE_NAME))
        time.sleep(3)
        if self.get_app_id():
            print("APP_NAME: {} is success start.".format(app_name))
        else:
            print("APP_NAME: {} is failure start.".format(app_name))

    def stop(self):
        app_id = self.get_app_id()
        if app_id:
            self.shell('kill -9 {}'.format(app_id))
        time.sleep(3)

    def start_status(self):
        if self.get_app_id():
            print("APP_NAME: {} is success on running.".format(app_name))
        else:
            print("APP_NAME: {} is failed on running.".format(app_name))

    def stop_status(self):
        if self.get_app_id():
            print("APP_NAME: {} is failed on stop.".format(app_name))
        else:
            print("APP_NAME: {} is success on stop.".format(app_name))

    def health_check(self):
        print("APP_NAME: {} is success health.".format(app_name))


if __name__ == '__main__':
    deploy = Deploy()
    if action == 'fetch':
        deploy.fetch()
    elif action == 'deploy':
        deploy.deploy()
    elif action == 'rollback':
        deploy.rollback()
    elif action == 'stop':
        deploy.stop()
    elif action == 'start':
        deploy.start()
    elif action == 'start_status':
        deploy.start_status()
    elif action == 'stop_status':
        deploy.stop_status()
    elif action == 'health_check':
        deploy.health_check()
    else:
        print("APP_NAME: {} action is wrong.".format(app_name))
        sys.exit(1)

