from django.core.management.base import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    help = "Создание тестовых продуктов"

    def handle(self, *args, **kwargs):
        products_data = [
            {"name": "Ноутбук", "description": "Мощный ноутбук для работы", "price": 1200.00, "stock_quantity": 10},
            {"name": "Телефон", "description": "Смартфон с хорошей камерой", "price": 800.00, "stock_quantity": 25},
            {"name": "Наушники", "description": "Беспроводные наушники", "price": 150.00, "stock_quantity": 50},
            {"name": "Планшет", "description": "Планшет для учебы", "price": 350.00, "stock_quantity": 15},
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "price": data["price"],
                    "stock_quantity": data["stock_quantity"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан продукт: {product.name}"))
            else:
                self.stdout.write(f"Продукт уже существует: {product.name}")

        self.stdout.write(self.style.SUCCESS("✅ Продукты созданы!"))
