from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from shopapp.models import Product, Order, OrderItem  # <-- ИСПРАВЛЕНО


class OrderDetailViewTestCase(TestCase):
    """Тесты для OrderDetailView"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_user',
            password='testpassword'
        )
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(
            codename='view_order',
            content_type=content_type
        )
        cls.user.user_permissions.add(permission)

    def setUp(self):
        self.client = Client()
        self.client.login(username='test_user', password='testpassword')

        self.product = Product.objects.create(
            name='Тестовый продукт',
            price=100.00,
            stock_quantity=10
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='ул. Тестовая, д. 1',
            comment='Тестовый комментарий'
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    @classmethod
    def tearDownTestData(cls):
        cls.user.delete()

    def test_order_details(self):
        url = reverse('shopapp:order_detail', args=[self.order.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.comment)
        self.assertEqual(response.context['order'].pk, self.order.pk)
