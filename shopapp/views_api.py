from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Поиск
    search_fields = ['name', 'description']
    
    # Сортировка
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']
    ordering = ['name']
    
    def perform_create(self, serializer):
        """При создании продукта добавляем создателя"""
        serializer.save(created_by=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Order"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    # Фильтрация
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'user__username', 'delivery_address']
    
    # Сортировка
    ordering_fields = ['id', 'user', 'created_at', 'delivery_address']
    ordering = ['-created_at']
