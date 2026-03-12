# celery_tasks/order/tasks.py
import time
import random
from datetime import datetime, timedelta
from celery_tasks.main import app
from apps.products.model import Order


# -------------------------- 同步函数：生成订单编号 --------------------------
def generate_order_sn():
    """
    生成唯一订单编号：时间戳 + 随机数 + 用户ID后4位（如果传了user_id）
    """
    # 1. 时间戳（精确到秒）
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # 2. 6位随机数
    random_num = random.randint(100000, 999999)
    # 3. 拼接成唯一订单号
    order_sn = f"{timestamp}{random_num}"
    return order_sn


# -------------------------- 异步任务：取消超时未支付订单 --------------------------
@app.task(bind=True, retry_backoff=3, retry_kwargs={'max_retries': 3})
def cancel_order_task(self, order_id):
    """
    异步取消超时订单（默认15分钟未支付）
    :param order_id: 订单ID
    :return: 取消结果
    """
    try:
        # 1. 查询订单
        order = Order.objects.get(id=order_id, status=1)  # status=1：待支付
        # 2. 检查订单是否已支付（避免重复取消）
        if order.status != 1:
            return f"订单{order.order_sn}已支付，无需取消"

        # 3. 取消订单：更新状态 + 恢复库存
        order.status = 6  # status=6：已取消
        order.cancel_time = datetime.now()
        order.save()

        # 4. 恢复商品库存（可选，根据你的Inventory模型调整）
        for item in order.items.all():
            # 假设你有Inventory模型，字段：product_spec、stock
            from apps.inventories.model import Inventory
            inventory = Inventory.objects.get(product_spec=item.spec)
            inventory.stock += item.quantity
            inventory.save()

        return f"订单{order.order_sn}已取消，库存已恢复"

    except Order.DoesNotExist:
        return f"订单ID{order_id}不存在"
    except Exception as e:
        # 异常重试（最多3次，每次间隔3秒）
        self.retry(exc=e)


# -------------------------- 定时任务：清理过期订单（可选） --------------------------
@app.task
def clean_expired_orders():
    """定时清理超过30天的已取消/已完成订单（可选）"""
    expired_time = datetime.now() - timedelta(days=30)
    Order.objects.filter(
        status__in=[6, 4],  # 6=已取消，4=已完成
        updated_at__lt=expired_time
    ).delete()
    return f"清理过期订单完成，清理时间：{datetime.now()}"