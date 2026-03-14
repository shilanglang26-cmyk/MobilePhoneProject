from django.db import models


# 商品分类模型
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="分类名称")
    desc = models.CharField(max_length=200, blank=True, verbose_name="分类描述")
    sort = models.IntegerField(default=0, verbose_name="排序序号")
    is_show = models.BooleanField(default=True, verbose_name="是否显示")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name
        ordering = ["sort"]

    def __str__(self):
        return self.name


# 商品模型（增加分类外键）
class Goods(models.Model):
    # 关联分类
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="goods_list",
        verbose_name="商品分类"
    )
    name = models.CharField(max_length=100, verbose_name="商品名称")
    desc = models.TextField(blank=True, verbose_name="商品描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(default=0, verbose_name="库存")
    image = models.ImageField(upload_to="goods/", blank=True, verbose_name="商品图片")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]

    def __str__(self):
        return self.name
