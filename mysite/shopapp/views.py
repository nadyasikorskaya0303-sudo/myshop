from django.shortcuts import render
from .models import Product, Order


def shop_index(request):
    """Главная страница со ссылками"""
    return render(request, 'shopapp/shop_index.html')


def products_list(request):
    """Список продуктов"""
    products = Product.objects.all()
    return render(request, 'shopapp/products_list.html', {'products': products})


def orders_list(request):
    """Список заказов"""
    orders = Order.objects.all()
    return render(request, 'shopapp/orders_list.html', {'orders': orders})
