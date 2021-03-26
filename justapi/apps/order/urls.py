from django.urls import path, re_path, include
from . import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('pay', views.PayView, 'pay')
# router.register('buys', views.buyOrderView, 'buys')
urlpatterns = [
    path('', include(router.urls)),
    path('success/', views.SuccessView.as_view()),
    re_path('buys/(?P<pk>\d+)', views.buyOrderView.as_view())
    # order/success/ 下的，前端返回发送数据的路由
]
