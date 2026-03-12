from django.db import models

from utils.snowflake import snowflake_generator


class Category(models.Model):
    """商品分类表（三级分类，自关联）"""
    name = models.CharField(max_length=50, verbose_name="分类名称")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name="父分类")
    sort = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ["sort"]


class Product(models.Model):
    """商品表（基础信息）"""
    id = models.BigIntegerField(
        primary_key=True,
        default=snowflake_generator.generate_id,  # 注册时自动生成雪花ID
        editable=False,  # 禁止手动编辑
        verbose_name="商品ID（雪花ID）"
    )
    name = models.CharField(max_length=100, verbose_name="商品名称")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="所属分类")
    cover_image = models.ImageField(upload_to='products/covers/', verbose_name="封面图")
    detail = models.TextField(verbose_name="商品详情")  # 富文本编辑
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="基础价格")
    sales = models.IntegerField(default=0, verbose_name="销量")
    score = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, verbose_name="评分")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"


class ProductSpec(models.Model):
    """商品规格表（多规格：颜色、功率等）"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specs", verbose_name="关联商品")
    color = models.CharField(max_length=20, null=True, blank=True, verbose_name="颜色")
    power = models.CharField(max_length=20, null=True, blank=True, verbose_name="功率")
    model = models.CharField(max_length=50, verbose_name="适配机型")  # 如iPhone 15、华为Mate 60
    spec_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="规格价格")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU编码")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "商品规格"
        verbose_name_plural = "商品规格"


class ProductImage(models.Model):
    """商品多图表"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="关联商品")
    image = models.ImageField(upload_to='products/images/', verbose_name="商品图片")
    sort = models.IntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"