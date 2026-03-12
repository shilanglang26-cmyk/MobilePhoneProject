# celery_tasks/main.py
import os
from celery import Celery
from celery.schedules import crontab

# 设置Django环境变量（必须）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_shop.settings')

# 初始化Celery
app = Celery('phone_shop')

# 加载配置：从Django settings中读取CELERY_开头的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有app中的tasks.py文件
app.autodiscover_tasks(['celery_tasks.order'])

# 可选：配置定时任务（如每天清理过期订单）
app.conf.beat_schedule = {
    'clean-expired-products': {
        'task': 'celery_tasks.order.tasks.clean_expired_orders',
        'schedule': crontab(hour=0, minute=0),  # 每天凌晨执行
    },
}