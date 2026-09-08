from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import OrderImportForm
import csv


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_quantity', 'is_available', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_available',)
    ordering = ('name',)
    fieldsets = (
        ('Основная информация', {'fields': ('name', 'description')}),
        ('Цена и наличие', {'fields': ('price', 'stock_quantity', 'is_available')}),
    )
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'delivery_address')
    ordering = ('-created_at',)
    
    change_list_template = "admin/orders_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.import_csv, name='import_orders'),
        ]
        return custom_urls + urls
    
    def import_csv(self, request):
        if request.method == 'POST':
            form = OrderImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                
                created_count = 0
                for row in reader:
                    # Получаем ID товаров из CSV (колонка products_ids)
                    # Ожидаем формат: "1,2,3" или "1;2;3"
                    product_ids_str = row.get('products_ids', '')
                    product_ids = []
                    if product_ids_str:
                        # Разбиваем строку по запятой или точке с запятой
                        for pid in product_ids_str.replace(';', ',').split(','):
                            try:
                                product_ids.append(int(pid.strip()))
                            except ValueError:
                                pass
                    
                    # Создаём заказ
                    order = Order.objects.create(
                        user_id=row['user_id'],
                        delivery_address=row['delivery_address'],
                        comment=row.get('comment', '')
                    )
                    
                    # Добавляем товары в заказ (через ManyToMany поле products)
                    if product_ids:
                        products = Product.objects.filter(id__in=product_ids)
                        order.products.set(products)
                    
                    created_count += 1
                
                messages.success(request, f"Заказы успешно импортированы! Создано: {created_count}")
                return redirect('..')
        else:
            form = OrderImportForm()
        
        return render(request, 'admin/import_form.html', {'form': form})


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order',)
    search_fields = ('product__name',)
