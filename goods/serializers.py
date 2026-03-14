from rest_framework import serializers
from .models import Category, Goods


# 分类序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# 商品序列化器（返回分类信息）
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Goods
        fields = "__all__"
