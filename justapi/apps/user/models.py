from django.db import models
from course.models import Course
from justapi.utils.models import BaseModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telephone = models.CharField(max_length=11)
    icon = models.ImageField(upload_to='icon', default='icon/default.png')
    gender = models.IntegerField(choices=((0,'男'),(1,'女')), default=0)
    tencent = models.IntegerField(default=None, null=True)
    signature = models.CharField(max_length=64, default='你还没有填简介啊~~')



# 用户喜欢点赞表
class Praise(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    # 修改成这样
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time  = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    praise = models.BooleanField(default=False, verbose_name="用户点赞字段")
    user = models.ForeignKey(User, related_name='praise_user', on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="点赞用户")
    course = models.ForeignKey(Course,  related_name='praise_course',on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="点赞的课程")


# 用户评论表
class Comment(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    # 修改成这样
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time  = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    comment = models.TextField(max_length=2048, verbose_name="用户评论", null=True, blank=True)
    user = models.ForeignKey(User, related_name='comment_user', on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="评论的用户")
    course = models.ForeignKey(Course, related_name='comment_course', on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="评论的课程")

