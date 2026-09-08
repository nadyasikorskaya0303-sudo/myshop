from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from .forms import ProductForm, OrderForm
import os
import logging

# Настройка логгера
logger = logging.getLogger(__name__)


# ============================================================
# 1. СТАРЫЕ ФУНКЦИИ
# ============================================================

def shop_index(request):
    """Главная страница"""
    logger.info("Главная страница загружена")  # <-- ТЕСТОВЫЙ ЛОГ
    return render(request, 'shopapp/shop_index.html')


def products_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'shopapp/products_list.html', {'products': products})


def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'shopapp/orders_list.html', {'orders': orders})


MAX_FILE_SIZE = 1 * 1024 * 1024


def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Файл не выбран'}, status=400)
        file = request.FILES['file']
        if file.size > MAX_FILE_SIZE:
            return JsonResponse({'error': 'Файл слишком большой'}, status=400)
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': f'Файл "{file.name}" загружен!'})
    return render(request, 'shopapp/upload.html')


# ============================================================
# 2. CLASS-BASED VIEWS
# ============================================================

class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:products_list')
    permission_required = 'shopapp.can_add_product'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта с проверкой прав"""
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:products_list')
    permission_required = 'shopapp.can_edit_product'

    def test_func(self):
        product = self.get_object()
        if self.request.user.is_superuser:
            return True
        return product.created_by == self.request.user


class ProductArchiveView(DeleteView):
    model = Product
    template_name = 'shopapp/product_archive.html'
    success_url = reverse_lazy('shopapp:products_list')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_available = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" архивирован!')
        return redirect(self.success_url)


class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_delete.html'
    success_url = reverse_lazy('shopapp:orders_list')


# ============================================================
# 3. ЭКСПОРТ ЗАКАЗОВ В JSON
# ============================================================

class OrdersExportView(UserPassesTestMixin, View):
    """Экспорт заказов в JSON-формате"""

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        orders = Order.objects.all().select_related('user').prefetch_related('products')

        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'delivery_address': order.delivery_address,
                'comment': order.comment or '',
                'user_id': order.user.id,
                'products': [p.id for p in order.products.all()]
            })

        return JsonResponse({'orders': orders_data}, json_dumps_params={'ensure_ascii': False})

# ============================================================
# 4. RSS-ЛЕНТА
# ============================================================

from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Product


class LatestProductsFeed(Feed):
    title = "Новые продукты"
    link = "/products/"
    description = "Обновления каталога продуктов"

    def items(self):
        return Product.objects.filter(is_available=True).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description[:200]

    def item_link(self, item):
        return item.get_absolute_url()

# ============================================================
# 5. ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ (с кешированием)
# ============================================================

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class UserOrdersListView(LoginRequiredMixin, ListView):
    """Список заказов пользователя (с кешированием части шаблона)"""
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        """Получаем заказы конкретного пользователя"""
        user_id = self.kwargs.get('user_id')
        self.owner = get_object_or_404(User, pk=user_id)
        return Order.objects.filter(user=self.owner).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context

# ============================================================
# 6. ЭКСПОРТ ЗАКАЗОВ ПОЛЬЗОВАТЕЛЯ В JSON (с низкоуровневым кешированием)
# ============================================================

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import OrderForUserSerializer


def user_orders_export(request, user_id):
    """Экспорт заказов пользователя в JSON с кешированием"""
    
    # Генерируем ключ для кеша
    cache_key = f'user_orders_export_{user_id}'
    
    # Проверяем кеш
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return JsonResponse(cached_data, safe=False)
    
    # Если данных в кеше нет — загружаем из БД
    user = get_object_or_404(User, pk=user_id)
    orders = Order.objects.filter(user=user).order_by('id')
    
    # Сериализуем данные
    serializer = OrderForUserSerializer(orders, many=True)
    data = {
        'user_id': user.id,
        'username': user.username,
        'orders_count': orders.count(),
        'orders': serializer.data
    }
    
    # Сохраняем в кеш на 5 минут
    cache.set(cache_key, data, 300)
    
    return JsonResponse(data, safe=False)

# ============================================================
# 5. ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ (с кешированием)
# ============================================================

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class UserOrdersListView(LoginRequiredMixin, ListView):
    """Список заказов пользователя (с кешированием части шаблона)"""
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        """Получаем заказы конкретного пользователя"""
        user_id = self.kwargs.get('user_id')
        self.owner = get_object_or_404(User, pk=user_id)
        return Order.objects.filter(user=self.owner).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context
