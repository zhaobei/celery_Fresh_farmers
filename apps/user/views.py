from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.mail import send_mail
import re
from celery_tasks.tasks import send_register_active_enaile
from django.http import HttpResponse
from  django.conf import settings
from django.views.generic import View
from apps.user.models import User,Address
from apps.order.models import OrderInfo,OrderGoods
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate,login, logout
from django.template import RequestContext
from utils.mixin import LoginrequiredMixin
from django_redis import get_redis_connection
from apps.goods.models import GoodsSKU
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

# Create your views here.

# /user/register
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':
        # 显示注册页面
        return render(request,'register.html')
    else:
        # 注册处理
        user_name = request.POST.get('user_name')  # 接收用户名
        password = request.POST.get('pwd')  # 接收密码
        email = request.POST.get('email')  # 接收邮箱
        allow = request.POST.get('allow')
        # 进行数据的校验
        if not all([user_name, password,
                    email]):  # all方法 函数用于判断给定的可迭代参数 [user_name,password,email]中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 检验用户是否同意用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 此用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 业务处理：进行用户注册
        user = User.objects.create_user(username=user_name, email=email, password=password)
        user.is_active = 0
        user.save()

        # 返回应答
        return redirect(reverse('goods:index'))

def register_handle(request):
    '''进行注册chuli'''
    # 接收数据
    user_name = request.POST.get('user_name')  #  接收用户名
    password = request.POST.get('pwd')  #  接收密码
    email = request.POST.get('email')  #  接收邮箱
    allow = request.POST.get('allow')
    # 进行数据的校验
    if not all([user_name,password,email]):  #  all方法 函数用于判断给定的可迭代参数 [user_name,password,email]中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False
        return render(request, 'register.html', {'errmsg': '数据不完整'})
    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
    # 检验用户是否同意用户协议
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请同意协议'})
    # 校验用户名是否重复
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        #用户名不存在
        user = None
    if user:
        #此用户名已存在
        return render(request,'register.html',{'errmsg':'用户名已存在'})




    # 业务处理：进行用户注册
    user = User.objects.create_user(username=user_name,email=email,password=password)
    user.is_active = 0
    user.save()

    # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
    # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密  itsdangerous 签名加密模块
    # 加密用户身份信息生成激活token
    serializer=Serializer(settings.SECRET_KEY,3600)
    info = {'confirm':user.id}
    token = serializer.dumps(info)

    # 发邮件

    # 返回应答
    return redirect(reverse('goods:index'))

class RegisterView(View):
    '''注册类'''
    def get(self,request):
        '''显示注册页面'''
        return render(request,'register.html')
    def post(self,request):
        '''进行注册处理'''
        # 接收数据
        user_name = request.POST.get('user_name')  # 接收用户名
        password = request.POST.get('pwd')  # 接收密码
        email = request.POST.get('email')  # 接收邮箱
        allow = request.POST.get('allow')
        # 进行数据的校验

        if not all([user_name, password,
                    email]):  # all方法 函数用于判断给定的可迭代参数 [user_name,password,email]中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        # 检验用户是否同意用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 此用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        print("业务出里")
        # 业务处理：进行用户注册
        user = User.objects.create_user(username=user_name, email=email, password=password)
        user.is_active = 0
        user.save()

        print("数据存储完成")

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)  #返回的数据是bytes（字节流）
        token = token.decode('utf8')

        print("加密信息完成")

        # 发送邮件
        send_register_active_enaile.delay(email,user_name,token)

        print("邮件任务发出")
        # 返回应答
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            # 根据id 获取用户信息
            user = User.objects.get(id = user_id)
            user.is_active = 1
            user.save()

            # 激活成功，跳转到登陆页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse("激活信息已经过期")

# /user/login
class LoginView(View):
    '''登陆'''
    def get(self, request):
        '''显示登陆页面'''
        # 判断是否记住了用户名
        if 'username' not in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # 使用模板
        return render(request,'login.html',{'username':username,'checked':checked})
    def post(self,request):
        '''登陆校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        # 业务处理：登陆校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名和密码正确
            if user.is_active:
                # 用户已激活

                # 记录用户登陆状态
                login(request,user)
                # 获取登陆后要跳转的地址
                # 默认跳转到首页
                next_url = request.GET.get('next',reverse('goods:index')) #NOne

                # 跳转到next_url
                response = redirect(next_url) # HttpResponseRedirect的对象
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 需要记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                # 返回response应答
                return response





            else:
                # 用户未激活
                return render(request,'login.html',{'errmsg':'用户未激活，请激活您的账户'})
        else:
            return render(request,'login.html',{'errmsg':'用户名或者密码错误'})


        # 返回应答

# /user/logout
# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))
# /user
class UserInfoView(LoginrequiredMixin,View):
    '''用户中心-信息页'''
    def get(self, request):
        # page=user
        # 通过request.user.is_authenticated() 判断用户是否登陆，如果已经登陆返回ture 否则返回flase
        # 除了你给模板文件传递的模板变量之外，django框架会把request.user也传给模板文件

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)
        # 获取用户的历史浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host='192.168.248.128',port='6379',db=9)
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        # 获取用户最新浏览的五条商品id
        sku_ids = con.lrange(history_key,0,4)
        # 从数据库中查询用户浏览商品具体信息
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)
        # 遍历获取用户浏览的历史商品信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        # 组织上下文
        context = {'page':'user',
                   'address':address,
                   'goods_li':goods_li}




        return render(request,'user_center_info.html',context)

# /user/order
class UserOrderView(LoginrequiredMixin,View):
    '''用户中心-订单页'''
    def get(self, request,page):
        # page=order
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
        # 遍历获取订单商品的信息

        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)
            # 遍历order_skus计算商品的小计

            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page': order_page,
                   'pages': pages,
                   'page': 'order'}

        # 使用模板
        return render(request, 'user_center_order.html', context)




# /user/address
class AddressView(LoginrequiredMixin,View):
    '''用户中心-地址页'''
    def get(self, request):
        '''显示'''
        # page=address
        # 获取登陆用户对应的对象
        user = request.user
        # # 获取用户默认的收获地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收获地址
        #     address = None
        address = Address.objects.get_default_address(user)
        # 使用模板
        return render(request,'user_center_site.html',{'page':'address','address':address})
    def post(self,request):
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 校验数据
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理-地址添加
        # 如果用户已存在默认收获地址，添加的地址不作为默认收货地址，否则作为默认收获地址
        user = request.user
        # 获取用户默认的收获地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收获地址
        #     address = None
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True
        # 添加地址

        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)
        # 返回应答 刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式

#  user/analysi
class Data_analysi(LoginrequiredMixin,View):
    '''准备分析数据获取整理,制作数据接口对接前端'''
    # 这个类
    def get(self,request):
        user = request.user
        list = []
        # 条形图数据
        bar_x = []
        bar_y = []

        # 饼图数据
        sector_x = bar_x
        sector_y = []

        # 数据哭提取数据
        ty = GoodsSKU.objects.values()
        temp = []

        for name in ty:
            bar_x.append(name['name'])
        for sales in ty:
            bar_y.append(sales['sales'])

        for stock in ty:
            temp.append(str(stock['stock']))
        dict = {"'" + 'name' + "'" + ":" + "'" + m + "'" + "," + "'" + 'value' + "'" + ":" + n for m in sector_x for n
                in temp}
        for i in dict:
            new = '{' + i + '}'
            b = eval(new)
            sector_y.append(b)

        tiao_x = bar_x[0:8]
        tiao_y = bar_y[0:8]
        for dic in sector_y[7:12]:
            list.append(dic['name'])
        bing_x = list
        bing_y = sector_y[7:12]

        # 临时性跳转，用来测试
        # return redirect(reverse('goods:index'))
        # return JsonResponse({'res': 2, 'errmsg': '非法的支付方式'})
        # return JsonResponse({"bar_x": bar_x, "bar_y": bar_y,"sector_x":sector_x,"sector_y":sector_y})
        # 返回数据分析页面需要的json串
        return HttpResponse(json.dumps((tiao_x,tiao_y,bing_x, bing_y), ensure_ascii=False),content_type="application/json,charset=utf-8")



# user/charts
class Charts(LoginrequiredMixin,View):
    """数据分析页"""
    def get(self,request):
        return render(request, 'charts.html')


class Seeyou(View):
    """彩蛋页面"""
    def get(self,request):
        return render(request, 'seeyou.html')

# /user/indexs
class Indexs(View):
    """优化后登录页，新增分类登录-用户登录-商家登录-游客浏览-用户注册"""
    def get(self,request):
        return render(request, 'indexs.html')
