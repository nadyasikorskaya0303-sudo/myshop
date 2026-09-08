from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_available = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=50, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    class Meta:
        # Сортировка по умолчанию: сначала по цене (возрастание), затем по названию
        ordering = ['price', 'name']

        # Название таблицы в базе данных
        db_table = 'products'

        # Название + категория должны быть уникальными вместе
        unique_together = ['name', 'category']

        # Читаемые названия для админки
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
