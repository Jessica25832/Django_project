from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib import messages
from apps.qfauth.decorators import qf_superuser_required
from django.utils.decorators import method_decorator
@qf_superuser_required
def staff_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }
    return render(request,'cms/staffs.html',context=context)

@method_decorator(qf_superuser_required,name='dispatch')
class AddStaffView(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups':groups
        }
        return render(request,'cms/add_staff.html',context=context)
    def post(self,request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            #因为普通用户 is_staff 为false 首先变成True 可以登陆后台
            #加到指定的分组中 他就具备权限了
            #接收 前端分组复选框  getlist接收列表  get 接收单个值
            group_ids = request.POST.getlist('groups')
            #根据id 查出指定的分组
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            messages.info(request,message="该手机号不存在")
            return redirect(reverse('cms:add_staff'))
