from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializer


class CourseCategoryView(GenericViewSet,ListModelMixin):
    queryset = models.CourseCategory.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = serializer.CourseCategorySerializer


from .paginations import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
from .filters import MyFilter,CourseFilterSet
class CouresView(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = serializer.CourseModelSerializer

    pagination_class = PageNumberPagination

    # 过滤和排序
    # filter_backends=[DjangoFilterBackend,OrderingFilter,SearchFilter]
    # filter_backends=[DjangoFilterBackend,OrderingFilter,MyFilter]
    filter_backends=[DjangoFilterBackend,OrderingFilter]
    # # filter_backends=OrderingFilter
    ordering_fields=['id', 'price', 'students']
    # search_fields=['name']

    # filter_fields=['course_category']


    # # g同过django-filter扩展过滤
    # filter_backends = [DjangoFilterBackend]
    # # 原来是配置字段，现在配置类
    filter_class = CourseFilterSet


'''
django-filters指定以某个字段过滤有两种方式
第一种：
    配置类:
    filter_backends=[DjangoFilterBackend]
    配置字段：
    filter_fields=['course_category']
第二种：
    配置类:
    filter_backends=[DjangoFilterBackend]
    配置类：（自己写的类）
    class CourseFilterSet(FilterSet):
        class Meta:
            model=models.Course
            fields=['course_category']
    filter_class = CourseFilterSet
    
第三种：实现区间过滤
    class CourseFilterSet(FilterSet):
        # 课程的价格范围要大于min_price，小于max_price
        min_price = filters.NumberFilter(field_name='price', lookup_expr='gt')
        max_price = filters.NumberFilter(field_name='price', lookup_expr='lt')
        class Meta:
            model=models.Course
            fields=['course_category']
    配置类:
        filter_backends=[DjangoFilterBackend]
    配置类：（自己写的类）
        -filter_class = CourseFilterSet
'''




'''
排序：
按id正序倒叙排序，按price正序倒叙排列
使用：http://127.0.0.1:8000/course/free/?ordering=-id
配置类：
    filter_backends=[OrderingFilter]
配置字段：
    ordering_fields=['id','price']
    
    
内置过滤：
使用：http://127.0.0.1:8000/course/free/?search=39
按照price过滤（表自有的字段直接过滤）
配置类：
    filter_backends=[SearchFilter]
配置字段：
    search_fields=['price']
    
扩展：django-filter
安装：
支持自由字段的过滤还支持外键字段的过滤
http://127.0.0.1:8000/course/free/?course_category=1   # 过滤分类为1 （python的所有课程）
配置类:
    filter_backends=[DjangoFilterBackend]
配置字段：
    filter_fields=['course_category']


'''

#如何自定义排序或者过滤类




# 课程章节接口
class CourseChapterView(GenericViewSet,ListModelMixin):
    queryset = models.CourseChapter.objects.filter(is_delete=False,is_show=True)
    serializer_class = serializer.CourseChapterSerializer

    # 可以按照课程id来查
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']




# 搜索接口
class CouresSearchView(GenericViewSet,ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True)
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination

    filter_backends=[SearchFilter]
    search_fields=['name']







# 优秀课程接口
class CoursePopularView(GenericViewSet,ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = serializer.CoursePopularSerializer

    filter_backends=[DjangoFilterBackend,OrderingFilter,MyFilter]
    ordering_fields=['id', 'popular']
    filter_fields=['course_category']



# 实践项目课程接口
class CourseProjectView(GenericViewSet,ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True,project=True)
    serializer_class = serializer.CourseProjectSerializer
    pagination_class = PageNumberPagination
    filter_backends=[DjangoFilterBackend]
    filter_fields=['course_category']




