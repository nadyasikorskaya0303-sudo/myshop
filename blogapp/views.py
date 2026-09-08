from django.views.generic import ListView
from .models import Article


class ArticlesListView(ListView):
    """Список статей с оптимизированными запросами"""
    model = Article
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        """Оптимизация запросов к БД:
           - select_related для ForeignKey (автор, категория)
           - prefetch_related для ManyToManyField (теги)
           - defer для исключения поля content (не используется на странице)
        """
        return Article.objects.select_related('author', 'category') \
                              .prefetch_related('tags') \
                              .defer('content')
