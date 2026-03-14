from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import uuid
from .models import Order, Logistics
from cart.models import Cart
from .serializers import OrderSerializer


# 创建订单
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user, is_selected=True)
        if not cart_items:
            return Response({"code": 400, "msg": "购物车为空"})

        # 计算总价
        total_price = sum(item.goods.price * item.num for item in cart_items)
        # 生成订单号
        order_no = uuid.uuid4().hex
        # 创建订单
        order = Order.objects.create(user=user, order_no=order_no, total_price=total_price)
        # 创建物流
        Logistics.objects.create(order=order)
        # 清空选中的购物车
        cart_items.delete()
        return Response({"code": 200, "msg": "订单创建成功", "order_no": order_no})


# 模拟支付接口
class PayOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_no = request.data.get("order_no")
        order = Order.objects.get(order_no=order_no, user=request.user)

        if order.status != 0:
            return Response({"code": 400, "msg": "订单状态异常"})
        if request.user.balance < order.total_price:
            return Response({"code": 400, "msg": "余额不足"})

        # 模拟支付：扣除余额
        request.user.balance -= order.total_price
        request.user.save()
        # 修改订单状态
        order.status = 1
        order.save()
        return Response({"code": 200, "msg": "支付成功"})


# 物流状态查询（随机模拟更新）
class LogisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_no):
        order = Order.objects.get(order_no=order_no, user=request.user)
        logistics = order.logistics
        # 随机更新物流状态
        logistics.update_logistics_status()
        serializer = LogisticsSerializer(logistics)
        return Response({"code": 200, "data": serializer.data})