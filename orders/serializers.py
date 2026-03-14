from rest_framework import serializers
from .models import Order, Logistics


class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistics
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    logistics = LogisticsSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("order_no", "total_price", "status")