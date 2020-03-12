import time
from django.conf import settings
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")# project_name 项目名称
django.setup()

from celery_tasks.tasks import generate_static_index_html
print('1')

generate_static_index_html.delay()
print('2')

