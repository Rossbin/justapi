

from .celery import app


@app.task
def add(x,y):
    print(x,y)
    return x+y

# @app.task
# def updata_banner():
#
#     # 在脚本中调用django项目
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled15.settings")
#     import django
#     django.setup()
#
#     from app01 import models
#     from django.core.cache import cache
#     books = models.Book.objects.all()
#     print(books)
