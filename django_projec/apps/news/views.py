from django.db.models import Q
from django.shortcuts import render

from apps.news.form import PublicCommentForm
from .models import NewsCategory,News,Comment
from django.views.decorators.http import require_GET
from django.conf import settings
from .serializers import NewsSerializers,CommentSerializers
from utils import restful_res
from django.conf import settings
from django.http import Http404
from apps.qfauth.decorators import qf_login_required
# from . import PublicCommentForm
@require_GET
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    #newses = News.objects.all()[0:count]
    newses = News.objects.select_related('author','category').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses':newses,
        'categories':categories
    }
    return render(request,'news/index.html',context=context)

def news_list(request):
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))
    #1 0 3
    #2 3 6
    #3 6 9
    # start = (第几页-1)*每页显示的条数
    start = (page-1)* settings.ONE_PAGE_NEWS_COUNT
    end = start+ settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0 :
        newses = News.objects.all()[start:end]
        # newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.filter(category__id=category_id)[start:end]
        #newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
        #newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    serializer = NewsSerializers(newses,many=True)
    data = serializer.data
    return restful_res.result(data=data)

def news_detail(request,news_id):
    try:
        # news = News.objects.select_related('category','author').get(pk=news_id)
        # news = News.objects.get(pk=news_id)
        news = News.objects.select_related('category','author').prefetch_related("comments__author").get(pk=news_id)
        # comments = news.comments.all()
        # print(comments)
        context = {
            'news':news
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404


@qf_login_required
def pub_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerializers(comment)
        return restful_res.result(data=serializer.data)
    else:
        return restful_res.params_error(message=form.get_errors())

def search(request):
    q = request.POST.get('q')
    print(q)
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
        context = {
            'newses':newses
        }
    return render(request,'search/search1.html',context=context)