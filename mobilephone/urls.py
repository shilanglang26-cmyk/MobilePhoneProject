"""
URL configuration for mobilephone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mobilephone.settings import MEDIA_ROOT
from mobilephone.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户模块
    path('api/users/', include('users.urls')),
    # 商品模块
    path('api/goods/', include('goods.urls')),
    # 购物车模块
    path('api/cart/', include('cart.urls')),
    # 订单模块
    path('api/orders/', include('orders.urls')),
    # 配置默认首页
    path('', index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
