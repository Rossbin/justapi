
from celery import Celery

#

broker='redis://127.0.0.1:6379/1'  #broker任务队列

backend='redis://127.0.0.1:6379/2'   # 结构存储，执行完的结果存在这

app=Celery(__name__,broker=broker,backend=backend)


#添加任务(使用这个装饰器装饰，@app.task)
@app.task
def add(x,y):
    print(x,y)
    return x+y
# 用命令来执行
# 非windows
# 命令：celery worker -A celery_task -l info
# windows：
# pip3 install eventlet
# celery worker -A celery_task -l info -P eventlet