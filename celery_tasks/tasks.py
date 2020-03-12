# 使用celery
import os
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext
import time
import pymysql



# 在任务处理者一端加这几句
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()
import raven
import toml
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


with open('./config/config_env.toml') as f:
    config = toml.load(f)

ENV_REDIS_HOST = config['redis']['host']

#创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks',broker='redis://'+ENV_REDIS_HOST+':6379/8')

from apps.goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection

# 定义任务函数
@app.task
def send_register_active_enaile(to_email,user_name,token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '速农鲜生欢迎信息'
    message = ''
    # 发件人
    sender = settings.EMAIL_FROM
    # 收件人列表
    receiver = [to_email]

    # 直接通过message无法正确解析程html样式
    html_message = '<h1>%s,欢迎您成为速农鲜生注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://'%(user_name)+ENV_REDIS_HOST+':8000/user/active/%s">http://'%(token)+ENV_REDIS_HOST+':8000/user/active/%s</a>' % (token)
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=receiver, html_message=html_message)
    print("邮件发送")


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners



    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners,
               }

    # 使用模板
    # 1.加载模板文件
    temp=loader.get_template('static_index.html')

    # 2.模板渲染
    static_index_html = temp.render(context)
    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR,'static/index.html')

    with open(save_path,'w') as f:
        f.write(static_index_html)

