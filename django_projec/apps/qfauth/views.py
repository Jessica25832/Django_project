from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from django.shortcuts import reverse,redirect
from utils import restful_res
from django.contrib.auth import get_user_model
from utils.captcha.qfcaptcha import Captcha
from io import BytesIO
from django.core.cache import cache
from utils.aliyun_res import send_sms
# 通过当前用户模型获取当前用户
User = get_user_model()
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None) #None默认过期时间2周
                else:
                    request.session.set_expiry(0)
                return restful_res.success()
            else:
                return restful_res.unauth(message="您的账户被冻结")
        else:
            return restful_res.params_error(message="用户名或者密码错误")
    else:
        errors = form.get_errors()
        return restful_res.params_error(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('cms:index'))

@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful_res.success()
    else:
        return restful_res.params_error(message=form.get_errors())


# @require_POST
# def register_view(request):
#     form = RegisterForm(require_POST)
#     if form.is_valid():
#         telephone = form.cleaned_data.get('telephone')
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = User.objects.create_user(telephone=telephone,username=username,password=password)
#         login(request,user)
#         return restful_res.success()
#     else:
#         errors = form.get_errors()
#         return restful_res.params_error(message=errors)

def img_captcha(request):
    text,image = Captcha.gene_code()

    out = BytesIO()

    image.save(out,'png')
    out.seek(0)

    response = HttpResponse(content_type='image/png')

    response.write(out.read())
    response['Content-lenth'] = out.tell()

    # 存入缓存里，过期时间是5分钟
    cache.set(text.lower(),text.lower(),5*60)

    return response

def sms_captcha(request):
    telephone = request.GET.get('telephone')

    text = Captcha.gene_text()

    cache.set(telephone,text.lower(),5*60)
    print('短信验证码：',text)
    send_sms(telephone,text)
    return restful_res.success()


def cache_test(request):
    cache.set('username','kangbazi',60)
    result = cache.get('username')
    print(result)
    return HttpResponse('OK')