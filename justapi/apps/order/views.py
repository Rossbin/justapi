from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin      # 重写了create方法
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from . import models
from . import serializer
from utils.response import APIResponse

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
        from justapi.libs.al_pay import alipay
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
            print('%s订单支付成功'%out_trade_no)
            return Response('success')
        else:
            log.info('%s订单有问题' % out_trade_no)
            print('%s订单有问题' % out_trade_no)
            return Response('error')



from rest_framework.exceptions import APIException
from .paginations import PageNumberPagination
class buyOrderView(APIView):
    authentication_classes = [JSONWebTokenAuthentication,]      # 使用JWT认证类，有问题：需要配合一个权限类
    permission_classes = [IsAuthenticated,]                     # 配合JWT，必须登录后才能进入

    # queryset = models.Order
    # serializer_class = serializer.BuyOrderSerializer

    def get(self,request,pk,*args,**kwargs):
        order = models.Order.objects.all().filter(user=pk,order_status=True).order_by('id')   # 这里如果不加这个东西会报错

        # 分页
        page_cursor = PageNumberPagination()
        order = page_cursor.paginate_queryset(order,request,view=self)
        next_url = page_cursor.get_next_link()
        pr_url = page_cursor.get_previous_link()
        count = page_cursor.page.paginator.count

        # print("下一页",next_url)
        # print("上一页",pr_url)


        order_ser = serializer.BuyOrderSerializer(order,many=True,context={'request':request})
        result = order_ser.data

        if result:
            return APIResponse(code=1,msg='获取成功',data=result,count=count,next=next_url,previou=pr_url)
        else:
            raise APIException()
