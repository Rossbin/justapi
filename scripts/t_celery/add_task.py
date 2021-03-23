



from celery_task import add

# add(3,4)  # 直接执行，不会被添加到broker中


ret=add.delay(5,4)  #想broker中添加一个任务
print(ret)