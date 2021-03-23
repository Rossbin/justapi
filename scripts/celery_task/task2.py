
from .celery import app


@app.task
def mutile(x,y):
    print(x,y)
    return x*y
