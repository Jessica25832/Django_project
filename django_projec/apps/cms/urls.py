from django.urls import path
from . import views
from . import staff_views
app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('news_list/',views.NewsListView.as_view(),name='news_list'),
    path('add_news_category/',views.add_news_category,name='add_news_category'),
    path('news_category/',views.news_category,name='news_category'),
    path('write_news/',views.WriteNewsView.as_view(),name='write_news'),
    path('edit_news/',views.editNewsView.as_view(),name='edit_news'),
    path('qntoken/',views.qiniu_token,name='qntoken')
]


#员工管理的url
urlpatterns += [
    path('staffs/', staff_views.staff_view, name='staffs'),
    path('add_staff/', staff_views.AddStaffView.as_view(), name='add_staff'),

]