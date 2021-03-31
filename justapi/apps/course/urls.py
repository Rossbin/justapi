from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('categories', views.CourseCategoryView, 'categories')
router.register('free', views.CouresView, 'free')
router.register('chapters', views.CourseChapterView, 'coursechapter')
router.register('search', views.CouresSearchView, 'search')
# router.register('teacher', views.CourseTeacherView, 'teacher')
router.register('popular', views.CoursePopularView, 'popular')
router.register('project', views.CourseProjectView, 'project')
urlpatterns = [
    path('', include(router.urls)),

]
