from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_api import ProductViewSet, OrderViewSet

# Создаём роутер для API
router = DefaultRouter()
router.register(r'api/products', ProductViewSet, basename='product')
router.register(r'api/orders', OrderViewSet, basename='order')

app_name = 'shopapp'

urlpatterns = [
    # Главная
    path('', views.shop_index, name='shop_index'),

    # Продукты
    path('products/', views.products_list, name='products_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', views.ProductArchiveView.as_view(), name='product_archive'),

    # Заказы
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # Экспорт заказов
    path('orders/export/', views.OrdersExportView.as_view(), name='orders_export'),

    # Загрузка файлов
    path('upload/', views.upload_file, name='upload_file'),

    # RSS-лента
    path('products/latest/feed/', views.LatestProductsFeed(), name='products_feed'),

    # Заказы пользователя (с кешированием)
    path('users/<int:user_id>/orders/', views.UserOrdersListView.as_view(), name='user_orders'),

    # Экспорт заказов пользователя в JSON
    path('users/<int:user_id>/orders/export/', views.user_orders_export, name='user_orders_export'),

    # API (DRF)
    path('', include(router.urls)),
]
