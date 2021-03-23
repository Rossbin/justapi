

from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self,code=1,msg='成功',result=None,status=None,headers=None,content_type=None,**kwargs):
        # code1表示成功，0表示失败

        dic = {
            'code':code,
            'msg': msg
        }
        if result:
            dic['result'] = result
        dic.update(kwargs)
        super().__init__(data=dic,status=status,headers=headers,content_type=content_type)
