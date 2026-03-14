from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义用户模型（新增余额字段）
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="账户余额")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 用户地址模型
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="用户")
    receiver = models.CharField(max_length=20, verbose_name="收件人")
    phone = models.CharField(max_length=11, verbose_name="收件电话")
    address = models.CharField(max_length=200, verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name="默认地址")

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name
