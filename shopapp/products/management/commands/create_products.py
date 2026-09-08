from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Создание тестовых товаров'

    def handle(self, *args, **kwargs):
        products_data = [
            {'name': 'Книга', 'price': 500, 'description': 'Интересная книга'},
            {'name': 'Ручка', 'price': 50, 'description': 'Шариковая ручка'},
            {'name': 'Тетрадь', 'price': 100, 'description': 'Тетрадь в клетку'},
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'price': data['price'],
                    'description': data['description'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создан товар: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Товар уже существует: {product.name}'))

        self.stdout.write(self.style.SUCCESS('✅ Готово!'))
