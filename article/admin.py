from django.contrib import admin
from .models import *


class ArticleLine(admin.StackedInline):
    model = Comments
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    # Отображаемые поля
    fields = ['article_title', 'browser_url', 'article_image',
              'article_text', 'article_date']
    # Порядок вывода названий на начальной старнице
    ordering = ['id']
    inlines = [ArticleLine]
    list_filter = ['article_date']


admin.site.register(Article, ArticleAdmin)
