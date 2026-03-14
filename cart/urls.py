from django.urls import path
from . import views

urlpatterns = [
    # 购物车 增删改查
    path('', views.CartView.as_view({
        'get': 'list',      # 获取购物车列表
        'post': 'create'    # 加入购物车
    })),
    path('<int:pk>/', views.CartView.as_view({
        'put': 'update',     # 修改商品数量
        'delete': 'destroy'  # 删除购物车商品
    })),
]