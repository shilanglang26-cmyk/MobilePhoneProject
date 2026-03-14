from django.db import models
from users.models import User
from goods.models import Goods


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    num = models.IntegerField(default=1, verbose_name="购买数量")
    is_selected = models.BooleanField(default=True, verbose_name="是否选中")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 一个用户对一个商品只能有一条记录