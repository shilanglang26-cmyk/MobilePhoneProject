from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('manage/', views.UserManageView.as_view(), name='user-manage'),
    path('address/', views.AddressView.as_view({
        'get': 'list',  # 获取地址列表
        'post': 'create'  # 新增地址
    })),
    # 单个地址
    path('address/<int:pk>/', views.AddressView.as_view({
        'get': 'retrieve',  # 查询单个地址详情
        'put': 'update',  # 修改地址
        'delete': 'destroy'  # 删除地址
    })), ]
