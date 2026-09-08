from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from shopapp.models import Product, Order, OrderItem


class OrdersExportTestCase(TestCase):
    """Тесты для OrdersExportView"""
    
    def setUp(self):
        """Создаём тестовые данные перед каждым тестом"""
        self.client = Client()
        
        # Создаём staff-пользователя
        self.user = User.objects.create_user(
            username='staff_user',
            password='staffpass',
            is_staff=True
        )
        self.client.login(username='staff_user', password='staffpass')
        
        # Создаём продукты
        self.product1 = Product.objects.create(
            name='Продукт 1',
            price=100.00,
            stock_quantity=10,
            is_available=True
        )
        self.product2 = Product.objects.create(
            name='Продукт 2',
            price=200.00,
            stock_quantity=5,
            is_available=True
        )
        
        # Создаём заказ
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='ул. Тестовая, д. 2',
            comment='Тестовый заказ'
        )
        
        # Добавляем товары в заказ
        OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=1
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=3
        )
    
    def tearDown(self):
        """Удаляем данные после каждого теста"""
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        self.user.delete()
    
    def test_orders_export(self):
        """Проверяем экспорт заказов в JSON"""
        url = reverse('shopapp:orders_export')
        response = self.client.get(url)
        
        # Проверяем статус ответа
        self.assertEqual(response.status_code, 200)
        
        # Проверяем Content-Type
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Получаем данные из ответа
        response_data = response.json()
        self.assertIn('orders', response_data)
        
        # Получаем данные из БД и формируем ожидаемую структуру
        orders = Order.objects.all().select_related('user').prefetch_related('products')
        expected_orders = []
        for order in orders:
            expected_orders.append({
                'id': order.id,
                'delivery_address': order.delivery_address,
                'comment': order.comment or '',
                'user_id': order.user.id,
                'products': [p.id for p in order.products.all()]
            })
        
        # Сравниваем структуру целиком
        self.assertEqual(response_data['orders'], expected_orders)
