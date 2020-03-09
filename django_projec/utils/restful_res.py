#restful风格统一返回 json

#返回示例
#{"code":400,"message":"","data":{"name":""}}
from django.http import JsonResponse
class HttpCode(object):
    success = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

#统一返回的方法
def result(code=HttpCode.success,message="",data=None,kwargs=None):
    json_dict = {"code":code,"message":message,"data":data}
    #如果想返回除了code message data之额外的参数 那么 需要更新json_dict
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

#成功
def success():
    return result()

#参数错误 400 message data 需要在视图函数中传递过来
def params_error(message="",data=None):
    return result(code=HttpCode.paramserror,message=message,data=data)

#认证错误 401 message data 需要在视图函数中传递过来
def unauth(message="",data=None):
    return result(code=HttpCode.unauth,message=message,data=data)

#请求方法错误
def method_error(message="",data=None):
    return result(code=HttpCode.methoderror,message=message,data=data)

#服务器错误
def server_error(message="",data=None):
    return result(code=HttpCode.servererror,message=message,data=data)