from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # 导入JWT认证模块
from rest_framework.permissions import IsAuthenticated  # 配合JWT的权限类
from rest_framework.exceptions import ValidationError

from . import serializer  # 序列化器
from justapi.utils.response import APIResponse
from rest_framework.decorators import action
from . import models


class LoginView(ViewSet):
    @action(methods=('post',), detail=False)
    def login(self, request, *args, **kwargs):
        ser = serializer.UserSerilaizer(data=request.data)  # 将前端传回的数据序列化
        if ser.is_valid():
            token = ser.context['token']
            # ser.context['user'] 是user对象
            username = ser.context['user'].username
            queryset = models.User.objects.filter(username=username).first()
            serializer_class = serializer.UserSerilaizer(queryset)
            # user_ser = serializer.UserSerilaizer(queryset)
            # print(user_ser.data)
            # icon = ser.context['user'].icon
            # user = ser.context['user']
            # print('user',user.icon)

            # {'code':1
            #  msg:'chengg'
            #  token:'sdfasdf'
            #  username:'root'
            #  }
            return APIResponse(token=token, username=username, icon=serializer_class.data['icon'],
                               id=serializer_class.data['id'])
        else:
            return APIResponse(code=0, msg=ser.errors)

    @action(detail=False)
    def check_telephone(self, request, *args, **kwargs):
        import re
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1)
        except:
            return APIResponse(code=0, msg='手机号不存在')
        # 若前端收到的code=1就为注册过的，为0就为没有注册过

    @action(methods=['POST'], detail=False)
    def code_login(self, request, *args, **kwargs):
        ser = serializer.CodeUserSerilaizer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0, msg=ser.errors)


from .throttlings import SMSThrotting


class SendSmSView(ViewSet):
    throttle_classes = [SMSThrotting, ]

    @action(methods=['GET'], detail=False)
    def send(self, request, *args, **kwargs):
        '''
        发送验证码接口
        :return:
        '''
        import re
        from justapi.libs.tx_sms import get_code, send_message
        from django.core.cache import cache
        from django.conf import settings
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        code = get_code()
        result = send_message(telephone, code)
        # 验证码保存（保存到哪？）
        # sms_cache_%s
        cache.set(settings.PHONE_CACHE_KEY % telephone, code, 180)
        if result:
            return APIResponse(code=1, msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败')


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserRegisterSerilaizer

    # def create(self, request, *args, **kwargs):
    #     ser=self.get_serializer(data=request.data)
    #     if ser.is_valid():
    #         ser.save()
    #         return APIResponse(code=1,msg='注册成功',username=ser.data.get('username'))
    #     else:
    #         return APIResponse(code=0, msg=ser.errors)
    #

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get('username')
        return APIResponse(code=1, msg='注册成功', username=username)


class getUserView(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication, ]  # 使用JWT认证类，有问题：需要配合一个权限类
    permission_classes = [IsAuthenticated, ]  # 配合JWT，必须登录后才能进入
    queryset = models.User.objects.all()
    serializer_class = serializer.GetUserserializer

    def get(self, request, pk):
        return APIResponse(self.retrieve(request, pk))

    def patch(self, request, pk):
        return APIResponse(self.update(request, pk))


class PassWord(APIView):
    authentication_classes = [JSONWebTokenAuthentication, ]  # 使用JWT认证类，有问题：需要配合一个权限类
    permission_classes = [IsAuthenticated, ]  # 配合JWT，必须登录后才能进入

    def post(self, request):
        # 获取参数
        username = request.POST.get('username')
        true_password = request.POST.get('truepass')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        # 获得请求用户
        user = models.User.objects.get(username=username)

        if not user:
            raise ValidationError('没有该用户')
        # print(username)
        # print(password)
        ret = user.check_password(true_password)
        if not password == re_password:
            raise ValidationError('两次密码不一致')
        if not ret:
            raise ValidationError('密码错误')

        # 修改密码为新密码
        user.set_password(password)
        user.save()

        # 返回数据
        return APIResponse(code=1, msg="成功")


# 点赞接口
class PraiseView(GenericViewSet, APIView):
    queryset = models.Praise.objects.all()
    serializer_class = serializer.UserPraiseSerilaizer

    def update(self, request):
        re_data = request.data
        user = re_data['user']
        course = re_data['course']
        praise = models.Praise.objects.filter(user=user, course=course).first()
        if not praise:
            return APIResponse(code=0, msg='获取失败')
        else:
            praise_ser = serializer.UserPraiseSerilaizer(instance=praise, data=request.data, partial=True)
            praise_ser.is_valid(raise_exception=True)
            praise_ser.save()
            result = praise_ser.data
            praise = str(re_data['praise'])
            print(praise)
            if praise == "True":
                p_course = models.Course.objects.filter(id=course).first()
                popular = p_course.popular + 10
                models.Course.objects.filter(id=course).update(popular=popular)
                print("true",popular)
            else:
                p_course = models.Course.objects.filter(id=course).first()
                popular = p_course.popular - 10
                models.Course.objects.filter(id=course).update(popular=popular)
                print("false",popular)
            return APIResponse(code=1, msg='获取成功', data=result)



    def get(self, request):
        re_data = request.data
        user = re_data['user']
        course = re_data['course']
        praise = models.Praise.objects.filter(user=user, course=course).first()
        if not praise:
            return APIResponse(code=0, msg='获取失败')
        else:
            praise_ser = serializer.UserPraiseSerilaizer(instance=praise, data=request.data, partial=True)
            praise_ser.is_valid(raise_exception=True)
            result = praise_ser.data
            return APIResponse(code=1, msg='获取成功', data=result)





# 评论接口
class CommentView(GenericViewSet,  APIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializer.CommentSerializer
    def get(self,request):
        # print("get",request.data)
        re_data = request.data
        course_id = re_data['course']
        comment_list = models.Comment.objects.filter(course=course_id).all()
        if not comment_list:
            return APIResponse(code=0,msg='获取失败')
        else:
            comment_list_ser = serializer.CommentSerializer(instance=comment_list,many=True)
            return APIResponse(code=1,msg='获取成功',data=comment_list_ser.data)



    def update(self, request):
        # print("update",request.data)
        re_data = request.data
        user = re_data['user']
        course = re_data['course']
        comment = models.Comment.objects.filter(user=user, course=course).first()
        if not comment:
            return APIResponse(code=0, msg='获取失败')
        else:
            praise_ser = serializer.CommentSerializer(instance=comment, data=request.data, partial=True)
            praise_ser.is_valid(raise_exception=True)
            praise_ser.save()
            result = praise_ser.data
            return APIResponse(code=1, msg='获取成功', data=result)

