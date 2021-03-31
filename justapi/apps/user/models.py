from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telephone = models.CharField(max_length=11)
    icon = models.ImageField(upload_to='icon', default='icon/default.png')
    gender = models.IntegerField(choices=((0,'男'),(1,'女')), default=0)
    tencent = models.IntegerField(default=None, null=True)
    signature = models.CharField(max_length=64, default='你还没有填简介啊~~')
