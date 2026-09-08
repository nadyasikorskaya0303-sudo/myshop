from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('orders/', views.order_list, name='orders'),  # 👈 Добавьте эту строку
]
