from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 
                  'is_available', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для позиций заказа"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов"""
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'delivery_address', 'comment', 
                  'created_at', 'items']
        read_only_fields = ['id', 'created_at']

class OrderForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов пользователя (без вложенных объектов)"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_ids = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'delivery_address', 
                  'comment', 'created_at', 'product_ids']
        read_only_fields = ['id', 'created_at']
    
    def get_product_ids(self, obj):
        return [p.id for p in obj.products.all()]

class OrderForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов пользователя (без вложенных объектов)"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_ids = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_username', 'delivery_address', 
                  'comment', 'created_at', 'product_ids']
        read_only_fields = ['id', 'created_at']
    
    def get_product_ids(self, obj):
        return [p.id for p in obj.products.all()]
