from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django_redis import get_redis_connection
from rest_framework.response import Response

from .models import Category, Goods
from .serializers import CategorySerializer, GoodsSerializer

redis_conn = get_redis_connection("default")


# 商品分类接口
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_show=True)
    serializer_class = CategorySerializer


# 商品接口（支持图片上传）
class GoodsView(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 允许表单+文件上传（核心！）
    parser_classes = (MultiPartParser, FormParser,)

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "desc"]
    ordering_fields = ["price", "create_time", "stock"]

    def get_queryset(self):
        queryset = Goods.objects.all()
        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id", "all")
        cache_key = f"hot_goods_{category_id}"
        cache_data = redis_conn.get(cache_key)
        if cache_data:
            return Response({"code": 200, "data": eval(cache_data)})
        response = super().list(request, *args, **kwargs)
        redis_conn.setex(cache_key, 600, str(response.data))
        return Response({"code": 200, "data": response.data})