from rest_framework import serializers
from .models import Cart
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(read_only=True)
    goods_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "goods", "goods_id", "num", "is_selected")
        read_only_fields = ("user",)