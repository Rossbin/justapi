from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin      # 重写了create方法
from . import models
from . import serializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication     # 导入JWT认证模块
from rest_framework.permissions import IsAuthenticated                       # 配合JWT的权限类
from rest_framework.response import Response
from rest_framework.views import APIView       # 在处理支付宝支付后前端异步回调接口不用再配置路由post get
class PayView(GenericViewSet,CreateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证类，有问题：需要配合一个权限类
    permission_classes = [IsAuthenticated,]                     # 配合JWT，必须登录后才能进入
    queryset = models.Order.objects.all()
    serializer_class = serializer.OrderSerializer

    # 重写create方法，在serializer中要传入request在user方法中
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.context.get('pay_url'))



class SuccessView(APIView):
    def get(self,request,*args,**kwargs):
        out_trade_no=request.query_params.get('out_trade_no')       # query_params字典
        order=models.Order.objects.filter(out_trade_no=out_trade_no).first()
                # 测试环境数据库的回调
        models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1)

        if order.order_status==1:
            return Response(True)
        else:
            return Response(False)

    def post(self,request,*args,**kwargs):
        '''
        支付宝回调接口
        '''
        from justapi.libs.al_pay.pem import alipay
        from justapi.utils.logger import log
        # 注意这个小细节,把他转成字典
        data = request.data.dict()
        out_trade_no=data.get('out_trade_no',None)
        gmt_payment=data.get('gmt_payment',None)
        signature = data.pop("sign")
        # 验证签名
        success = alipay.verify(data, signature)

        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1,pay_time=gmt_payment)
            log.info('%s订单支付成功'%out_trade_no)
            # print('%s订单支付成功'%out_trade_no)
            return Response('success')
        else:
            log.info('%s订单有问题' % out_trade_no)
            # print('%s订单有问题' % out_trade_no)
            return Response('error')