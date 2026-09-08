from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'stock_quantity': 'Количество на складе',
            'is_available': 'Доступен',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'delivery_address', 'comment', 'products']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'products': forms.SelectMultiple(attrs={'size': 5}),
        }
        labels = {
            'user': 'Пользователь',
            'delivery_address': 'Адрес доставки',
            'comment': 'Комментарий',
            'products': 'Товары',
        }

class OrderImportForm(forms.Form):
    """Форма для импорта заказов из CSV"""
    csv_file = forms.FileField(
        label="CSV файл с заказами",
        help_text="Колонки: user_id, delivery_address, comment, products_ids (ID товаров через запятую)"
    )
