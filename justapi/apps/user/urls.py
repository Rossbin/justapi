from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter    # 自动生成路由模块

router = SimpleRouter()
router.register('', views.LoginView, 'login')
router.register('', views.SendSmSView, 'send')
router.register('register', views.RegisterView, 'register')  # /user/register   post请求就是新增
router.register('getuser', views.getUserView, 'getuser')
# router.register('praise', views.PraiseView,'praise')
urlpatterns = [
    path('', include(router.urls)),
    path('retrieve/', views.PassWord.as_view()),
    path('praise/', views.PraiseView.as_view({'post':'get','patch':'update'})),
    path('comment/', views.CommentView.as_view({'post':'get','patch':'update'}))


]
