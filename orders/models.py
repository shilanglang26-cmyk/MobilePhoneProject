from django.db import models
from users.models import User
from goods.models import Goods
import random


# 订单模型
class Order(models.Model):
    STATUS_CHOICES = (
        (0, "待支付"),
        (1, "已支付/待发货"),
        (2, "已完成"),
        (3, "已取消"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    order_no = models.CharField(max_length=50, unique=True, verbose_name="订单号")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="订单状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

# 物流模型（随机模拟状态）
class Logistics(models.Model):
    STATUS_CHOICES = (
        (0, "待发货"),
        (1, "已发货"),
        (2, "运输中"),
        (3, "派送中"),
        (4, "已签收"),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="logistics", verbose_name="订单")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="物流状态")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "物流"
        verbose_name_plural = verbose_name

    # 模拟随机更新物流状态
    def update_logistics_status(self):
        if self.status < 4:
            self.status = random.randint(self.status + 1, 4)
            self.save()