from gevent import monkey
monkey.patch_all()
import multiprocessing

# 监听端口8000
bind = '0.0.0.0:8000'

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 工作模式协程
worker_class = 'gevent'
# 设置最大并发量
worker_connections = 2000
# 指定每个进程的线程数
threads = 2

# 设置守护进程(linux有效)
daemon = 'true'

# 下面这些没有的目录，要提前建好，不然出错
# 设置进程文件目录
pidfile = '/var/log/gunicorn/gunicorn.pid'
# 设置访问日志和错误信息日志路径
accesslog = '/var/log/gunicorn/logs/gunicorn_acess.log'
errorlog = '/var/log/gunicorn/logs/gunicorn_error.log'
# 设置日志记录水平
loglevel = 'debug'
