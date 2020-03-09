from django.http import Http404

from utils import restful_res
from django.shortcuts import redirect,reverse
def qf_login_required(func):
    def wrapper(request,*args,**kwargs):
    #     登录以后才去执行方法
        if request.user.is_authenticated:
            # 参数带着
            return func(request,*args,**kwargs)
        else:
    #         如果是ajax也要返回登录信息，告知
            if request.is_ajax():
                return restful_res.unauth(message="请先登录")
            else:
                # 如果不是ajax，给你跳转到首页
                return redirect(reverse('news:index'))

    return wrapper

def qf_superuser_required(func):
    def decorator(request,*args,**kwargs):
        if request.user.is_superuser:
            return func(request,*args,**kwargs)
        else:
            raise Http404()
    return decorator