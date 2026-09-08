from django.core.management.base import BaseCommand
from blogapp.models import Author, Category, Tag, Article
from django.utils import timezone


class Command(BaseCommand):
    help = "Создание тестовых данных для блога"

    def handle(self, *args, **kwargs):
        # Создаём авторов
        authors = []
        for name in ['Иван Иванов', 'Пётр Петров', 'Сергей Сергеев', 'Анна Смирнова']:
            author = Author.objects.create(name=name, bio=f"Биография автора {name}")
            authors.append(author)
            self.stdout.write(f"Создан автор: {name}")

        # Создаём категории
        categories = []
        for name in ['Технологии', 'Наука', 'Искусство', 'Путешествия', 'Кулинария']:
            category = Category.objects.create(name=name)
            categories.append(category)
            self.stdout.write(f"Создана категория: {name}")

        # Создаём теги
        tags = []
        for name in ['Python', 'Django', 'JavaScript', 'HTML', 'CSS', 'React', 'Vue']:
            tag = Tag.objects.create(name=name)
            tags.append(tag)
            self.stdout.write(f"Создан тег: {name}")

        # Создаём статьи
        articles_data = [
            {"title": "Введение в Django", "content": "Подробное введение в Django...", "author": authors[0], "category": categories[0]},
            {"title": "Что такое REST API", "content": "Объяснение REST архитектуры...", "author": authors[1], "category": categories[0]},
            {"title": "Новые открытия в космосе", "content": "Последние новости из космоса...", "author": authors[2], "category": categories[1]},
            {"title": "Искусство в современном мире", "content": "Тенденции современного искусства...", "author": authors[3], "category": categories[2]},
            {"title": "Путешествие по Европе", "content": "Маршруты и советы для путешествий...", "author": authors[0], "category": categories[3]},
            {"title": "10 рецептов быстрой кухни", "content": "Вкусные и простые рецепты...", "author": authors[1], "category": categories[4]},
            {"title": "JavaScript для начинающих", "content": "Основы JavaScript...", "author": authors[2], "category": categories[0]},
            {"title": "Горы vs Море", "content": "Куда поехать в отпуск...", "author": authors[3], "category": categories[3]},
        ]

        for data in articles_data:
            article = Article.objects.create(
                title=data["title"],
                content=data["content"],
                author=data["author"],
                category=data["category"],
                pub_date=timezone.now()
            )
            # Добавляем случайные теги
            article.tags.add(*tags[:3])
            self.stdout.write(f"Создана статья: {data['title']}")

        self.stdout.write(self.style.SUCCESS("✅ Тестовые данные созданы!"))
