from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product, OrderItem


class Command(BaseCommand):
    help = "Создание тестовых заказов"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="test_user",
            defaults={"email": "test@example.com"}
        )
        if created:
            user.set_password("test123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Создан пользователь: {user.username}"))

        products = Product.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR("Нет продуктов! Сначала выполните create_products"))
            return

        orders_data = [
            {"address": "ул. Ленина, д. 1", "comment": "Позвонить перед доставкой"},
            {"address": "ул. Пушкина, д. 10", "comment": "Вход со двора"},
            {"address": "ул. Гагарина, д. 5", "comment": ""},
        ]

        for data in orders_data:
            order, created = Order.objects.get_or_create(
                user=user,
                delivery_address=data["address"],
                defaults={"comment": data["comment"]}
            )

            if created:
                for product in products[:3]:
                    OrderItem.objects.get_or_create(
                        order=order,
                        product=product,
                        defaults={"quantity": 1}
                    )
                self.stdout.write(self.style.SUCCESS(f"Создан заказ #{order.id}"))
            else:
                self.stdout.write(f"Заказ уже существует: #{order.id}")

        self.stdout.write(self.style.SUCCESS("✅ Заказы созданы!"))
