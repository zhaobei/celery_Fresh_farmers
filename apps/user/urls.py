
from django.conf.urls import url,re_path
from django.contrib import admin
from apps.user import views

from django.contrib.auth.decorators import login_required
from apps.user.views import RegisterView,ActiveView,LoginView,UserInfoView, UserOrderView, AddressView,LogoutView,Data_analysi,Charts,Seeyou,Indexs   #导入类视图

urlpatterns = [
    # re_path(r'^register$',views.register,name='register'),  #注册
    # re_path(r'^register_handle$',views.register_handle,name='register_handle')  #注册处理
    re_path(r'^register$',RegisterView.as_view(),name='register'),  # 用户注册页
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    re_path(r'^login$',LoginView.as_view(),name = 'login'),  # 登陆
    re_path(r'^logout$',LogoutView.as_view(),name='logout'),  # 注销登陆

    # re_path(r'^$', login_required(UserInfoView.as_view()), name='user'),  # 用户中心-信息页
    # re_path(r'^order$', login_required(UserOrderView.as_view()), name='order'),  # 用户中心-订单页
    # re_path(r'^address$', login_required(AddressView.as_view()), name='address'),  # 用户中心-地址页

    re_path(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    re_path(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    re_path(r'^address$',AddressView.as_view(), name='address'),  # 用户中心-地址页
    re_path(r'analysi$',Data_analysi.as_view(), name='analysi'),   # 数据分析页
    re_path(r'charts$',Charts.as_view(), name='charts'),   # 数据分析页
    re_path(r'seeyou$',Seeyou.as_view(),name='seeyou'),  # 彩蛋页
    re_path(r'^indexs$',Indexs.as_view(),name='indexs' ),   # 优化导航登录页
]
