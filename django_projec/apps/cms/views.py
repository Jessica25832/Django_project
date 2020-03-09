from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST
from django.views.generic import View
from apps.news.models import NewsCategory,News,Comment
from utils import restful_res
from django.views.decorators.http import require_POST,require_GET
from .forms import WriteNewsForm,EditNewsForm
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.admin.views.decorators import staff_member_required
from urllib import parse  #拼接成 url地址
from apps.qfauth.decorators import qf_login_required
from django.utils.decorators import method_decorator
#{'start':'','end':''}
#http://127.0.0.1:8003/cms/news_list/?start=&end=&title=%E6%9D%9C%E5%BA%B7&category=0
from django.contrib.auth.decorators import permission_required
@require_GET
@staff_member_required(login_url='news:index')
def index(request):
    return render(request,'cms/index.html')


@method_decorator(permission_required(perm="news.change_news",login_url='/news'),name='dispatch')
class NewsListView(View):
    def get(self,request):
        #接收搜索条件内容
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category',0) or 0)
        page = int(request.GET.get('p',1))
        newses = News.objects.select_related('category', 'author')
        if start or end:
            if start:
                #js时间 解析成时间元祖
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=6,day=6)
            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_id:
            newses = newses.filter(category=category_id)


        # newses = News.objects.all()

        paginator = Paginator(newses,2) #paginator对象
        #page对象 是否有上一页下一页等
        page_obj = paginator.page(page) #参数为 用户想查看第几页

        context_data = self.get_pagination_data(paginator,page_obj)
        context = {
            'categories':NewsCategory.objects.all(),
            'newses':page_obj.object_list,
            'page_obj':page_obj,
            'paginator':paginator,
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id,
            'url_query':'&'+parse.urlencode({
                'start':start or '',
                'end':end or '',
                'title':title or '',
                'category':category_id or '',
            })
        }
        context.update(context_data)
        return render(request,'cms/news_list.html',context=context)

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_number = page_obj.number #当前页码
        num_pages = paginator.num_pages #总的页码

        left_has_more = False
        right_has_more = False

        if current_number <= around_count + 2:
            left_pages = range(1,current_number)
        else:
            left_has_more = True
            left_pages = range(current_number-around_count,current_number)
        #1 2 3 4 5 6      15 16 17 18 19 20
        if current_number >= num_pages-around_count - 1:
            right_pages = range(current_number+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_number+1,current_number+around_count+1 )

        return {
            'current_number':current_number,
            'num_pages':num_pages,
            'right_pages':right_pages,
            'left_pages':left_pages,
            'right_has_more':right_has_more,
            'left_has_more':left_has_more,

        }
#分类页面
@require_GET
@permission_required(perm="news.add_newscategory",login_url='/news')
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'cms/news_category.html',context=context)
#添加文章分类
@require_POST
@permission_required(perm="news.add_newscategory",login_url='/news')
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful_res.success()
    else:
        return restful_res.params_error(message='该分类已经存在')

#发布资讯
@method_decorator(permission_required(perm="news.add_news",login_url='/news'),name='dispatch')
class WriteNewsView(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories':categories
        }
        return render(request,'cms/write_news.html',context=context)
    def post(self,request):
        print(0)
        form = WriteNewsForm(request.POST)
        print(1)
        if form.is_valid():
            print(2)
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            thumbnail = form.cleaned_data.get('thumbnail')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            print(title,desc,content,thumbnail)
            News.objects.create(title=title,desc=desc,content=content,thumbnail=thumbnail,author=request.user,category=category)
            return restful_res.success()
        else:
            return restful_res.params_error(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news",login_url='/news'),name='dispatch')
#编辑文章 传过来 你想编辑哪一页
class editNewsView(View):
    def get(self,request):
        #接收每一篇文章的id
        news_id = request.GET.get('news_id')
        #从数据库中查出来
        news = News.objects.get(pk=news_id)
        #显示在页面上
        context = {
            'news':news,
            'categories':NewsCategory.objects.all(),
        }
        #如果修改  那么提交到后台
        return render(request,'cms/write_news.html',context=context)
    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            thumbnail = form.cleaned_data.get('thumbnail')
            pk = form.cleaned_data.get('pk')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title, desc=desc, content=content, thumbnail=thumbnail, author=request.user,
                                category=category)
            return restful_res.success()
        else:
            return restful_res.params_error(message=form.get_errors())




import qiniu
from django.conf import settings
def qiniu_token(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME

    q = qiniu.Auth(access_key,secret_key)
    token = q.upload_token(bucket)

    return restful_res.result(data={"token":token})