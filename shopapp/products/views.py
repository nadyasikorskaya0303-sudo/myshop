from django.shortcuts import render
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/product_list.html', context)

def order_list(request):
    orders = Order.objects.prefetch_related('items__product').all()
    context = {'orders': orders}
    return render(request, 'products/order_list.html', context)
