

# 自定义过滤规则
from rest_framework.filters import BaseFilterBackend

class MyFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # 真正的过滤规则
        # params=request.GET.get('teacher')
        # queryset.filter('''''')
        return queryset[:10]



from django_filters.filterset import FilterSet
from django_filters import filters

from . import models
class CourseFilterSet(FilterSet):
    # 课程的价格范围要大于min_price，小于max_price
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gt')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model=models.Course
        fields=['course_category']