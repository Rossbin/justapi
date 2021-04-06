from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('actualcourse', views.ActualCouresView, 'actualcourse')
router.register('basecourse', views.BaseCouresView, 'basecourse')
router.register('sidercategory', views.SiderGeneralCategoryView, 'sidercategory')
router.register('generalcategor', views.GeneralCategoryView, 'generalcategor')
router.register('categories', views.CourseCategoryView, 'categories')
router.register('free', views.CouresView, 'free')
router.register('chapters', views.CourseChapterView, 'coursechapter')
router.register('search', views.CouresSearchView, 'search')
router.register('popular', views.CoursePopularView, 'popular')

urlpatterns = [
    path('', include(router.urls)),

]
