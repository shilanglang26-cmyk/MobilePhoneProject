from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AddressViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    # 注册/登录/退出
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    # JWT Token刷新
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    # 路由器分发（地址/个人信息）
    path('', include(router.urls)),
]