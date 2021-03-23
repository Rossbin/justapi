from celery_task import app

from celery.result import AsyncResult

id = '3e397fd7-e0c1-4c5c-999c-2655a96793bb'
if __name__ == '__main__':
    async = AsyncResult(id=id, app=app)
    if async.successful():
        result = async.get()
        print(result)
    elif async.failed():
        print('任务失败')
    elif async.status == 'PENDING':
        print('任务等待中被执行')
    elif async.status == 'RETRY':
        print('任务异常后正在重试')
    elif async.status == 'STARTED':
        print('任务已经开始被执行')