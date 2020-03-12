
from django.conf.urls import url,re_path
from django.contrib import admin
from apps.goods.views import IndexView,DetailView,ListView



# urlpatterns = [
#     re_path(r'^ $',views.index,name='index')  # 首页
#
# ]
urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'), # 首页
    re_path(r'^$', IndexView.as_view(), name='index'), # 首页

    re_path(r'^goods/(?P<goods_id>\d+)$',DetailView.as_view(),name = 'detail'),  # 详情页
    re_path(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$',ListView.as_view(),name = 'list'),  #列表页



]
