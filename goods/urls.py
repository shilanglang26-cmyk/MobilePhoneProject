from django.urls import path
from . import views

urlpatterns = [
    # 分类CRUD
    path('category/', views.CategoryView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    # 单个分类（查询+修改+删除）
    path('category/<int:pk>/', views.CategoryView.as_view({
        'get': 'retrieve',  # 查询单个分类详情
        'put': 'update',  # 修改分类
        'delete': 'destroy'  # 删除分类
    })),

    # 商品：列表 + 新增
    path('', views.GoodsView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    # 单个商品：查询+修改+删除
    path('<int:pk>/', views.GoodsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]
