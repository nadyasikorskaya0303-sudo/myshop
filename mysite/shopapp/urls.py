from django.urls import path
from . import views

app_name = 'shopapp'

urlpatterns = [
    path('', views.shop_index, name='shop_index'),
    path('products/', views.products_list, name='products_list'),
    path('orders/', views.orders_list, name='orders_list'),
]
