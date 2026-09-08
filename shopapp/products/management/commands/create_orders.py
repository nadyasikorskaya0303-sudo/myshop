from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Создание тестовых заказов'

    def handle(self, *args, **kwargs):
        # Берем первого пользователя
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('❌ Нет пользователей! Создайте суперпользователя.'))
            return

        # Берем товары
        products = Product.objects.all()
        if not products:
            self.stdout.write(self.style.ERROR('❌ Нет товаров! Сначала добавьте товары.'))
            return

        # Создаем заказ
        order = Order.objects.create(
            user=user,
            total_price=0
        )

        # Добавляем товары в заказ
        total = 0
        for i, product in enumerate(products[:3], 1):
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=i
            )
            total += product.price * i

        order.total_price = total
        order.save()

        self.stdout.write(self.style.SUCCESS(f'✅ Создан заказ #{order.id} на сумму {total} руб.'))

        # Выводим информацию о заказе
        self.stdout.write(f'📦 Заказ #{order.id}:')
        for item in order.items.all():
            self.stdout.write(f'  - {item.product.name} x {item.quantity} = {item.product.price * item.quantity} руб.')
