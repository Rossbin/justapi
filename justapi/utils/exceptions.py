

# 重写方法,加上日志

# 'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
from rest_framework.views import exception_handler
# from justapi.utils import response
from .response import APIResponse
from .logger import log

def common_exceptions_handler(exc, context):
    # log.error('view是: %s, 错误是%s'%(str(context['view']),str(exc)))
    log.error('view是: %s, 错误是%s'%(context['view'].__class__.__name__,str(exc)))   # 取出类名
    ret = exception_handler(exc, context)
    if not ret:   # DRF内置处理不了，丢给Django的，我们来处理

        if isinstance(exc,KeyError):
            return APIResponse(code=0,msg='key error')
        return APIResponse(code=0,msg='error',result=str(exc))
    else:
        return APIResponse(code=0,msg='error',result=ret.data)










