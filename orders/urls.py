from django.urls import path
from . import views

urlpatterns = [
    # 创建订单
    path('create/', views.CreateOrderView.as_view(), name='order-create'),
    # 模拟支付
    path('pay/', views.PayOrderView.as_view(), name='order-pay'),
    # 查询物流状态（传订单号）
    path('logistics/<str:order_no>/', views.LogisticsView.as_view(), name='logistics'),
]