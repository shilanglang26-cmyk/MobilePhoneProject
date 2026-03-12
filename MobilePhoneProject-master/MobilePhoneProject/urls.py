"""
URL configuration for MobilePhoneProject project.

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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from django.conf import settings
# from django.conf.urls.static import static
from .views import index

# 导入DRF和Swagger文档
from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="手机配件销售系统API",  # 还原正常中文，不要转义
#         default_version='v1',
#         description="手机配件销售系统的RESTful API接口文档",  # 正常中文
#         terms_of_service="https://www.example.com/terms/",
#         contact=openapi.Contact(email="admin@example.com"),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # Django自带管理后台
    path('admin/', admin.site.urls),

    # API文档路由
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API v1版本路由（核心）
    path('api/v1/', include([
        path('users/', include('apps.users.urls')),
        # path('products/', include('apps.products.urls')),
        # path('carts/', include('apps.carts.urls')),
        # path('products/', include('apps.products.urls')),
        # path('payments/', include('apps.payments.urls')),
        # path('reviews/', include('apps.reviews.urls')),
    ])),

    # 配置默认首页
    path('', index),
]

# 开发环境媒体文件路由
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)