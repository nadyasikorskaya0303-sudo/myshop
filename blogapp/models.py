from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    bio = models.TextField(blank=True, verbose_name="Биография")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Автор"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Категория"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        verbose_name="Теги"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-pub_date']
