from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError    # 密码校验不成功的抛错

import re
from django.core.cache import cache
from django.conf import settings
class UserSerilaizer(serializers.ModelSerializer):
    username = serializers.CharField()       # 因为是唯一，所以得重写

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id']
        extra_kwargs = {                     # 校验内容
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):


        # 多种登录方式
        user = self._get_user(attrs)
        # 签发token
        token = self._get_token(user)
        # 放到context中，我在视图类中可以取出来
        self.context['token'] = token
        self.context['user'] = user

        return attrs

    # 获取user的函数
    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        import re
        if re.match('^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^.+@.+$', username):  # 邮箱
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')

    #
    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)  # 通过user对象获得payload
        token = jwt_encode_handler(payload)  # 通过payload获得token
        return token


class CodeUserSerilaizer(serializers.ModelSerializer):
    code=serializers.CharField()
    class Meta:
        model = models.User
        fields = ['telephone', 'code']

    def validate(self, attrs):
        user=self._get_user(attrs)
        # 用户存在，签发token
        token = self._get_token(user)
        # 将获取的token和user传回去，为的是可以在视图类中可以取出来
        self.context['token'] = token
        self.context['user'] = user
        return attrs


    def _get_user(self, attrs):

        telephone = attrs.get('telephone')
        code = attrs.get('code')

        # 取出原来的code
        cache_code=cache.get(settings.PHONE_CACHE_KEY%telephone)
        if code ==cache_code:
            # 验证码通过
            if re.match('^1[3-9][0-9]{9}$', telephone):
                user = models.User.objects.filter(telephone=telephone).first()
                if user:
                    # 把使用过的验证码删除
                    cache.set(settings.PHONE_CACHE_KEY % telephone,'')
                    return user
                else:
                    raise ValidationError('用户不存在')
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')


    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)  # 通过user对象获得payload
        token = jwt_encode_handler(payload)  # 通过payload获得token
        return token



class UserRegisterSerilaizer(serializers.ModelSerializer):
    code=serializers.CharField(max_length=4,min_length=4,write_only=True)
    class Meta:
        model = models.User
        fields = ['telephone', 'code','password','username']
        extra_kwargs = {
            'password': {'max_length': 18,'min_length':8},
            'username': {'read_only':True}
        }


    # code单独校验的局部钩子（不好写，因为手机号不好取）
    def validate(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        # 取出原来的code
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code or code=='1234':
            # 验证码通过
            if re.match('^1[3-9][0-9]{9}$', telephone):
                attrs['username']=telephone  # 把用户的名字设成手机号
                attrs.pop('code')
                return attrs
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')


    # 重写create方法
    def create(self, validated_data):
        user=models.User.objects.create_user(**validated_data)
        return user

