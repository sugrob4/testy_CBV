import os

from django.db import models
from django.conf import settings


def upload_image_path(instance, filename):
    pth = settings.MEDIA_URL[1:len(settings.MEDIA_URL)] + 'images_articles'
    if os.path.exists(pth + '/{}'.format(filename)):
        os.remove(pth + '/{}'.format(filename))
    return 'images_articles/{}'.format(filename)



class Article(models.Model):
    class Meta:
        db_table = 'article'

    article_title = models.CharField(max_length=200)
    # Для адресса статьи со словами в модели
    # обязательно должно быть поле `slug`
    browser_url = models.SlugField(max_length=150, default='')
    article_image = models.ImageField(
            upload_to=upload_image_path,
            max_length=150, blank=True, verbose_name='Изображения',
            default='no_image.png')
    article_text = models.TextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title


class Comments(models.Model):
    class Meta:
        db_table = 'comments'

    login_user = models.CharField(max_length=40, blank=True, verbose_name='Логин пользователя')
    email_user = models.EmailField(max_length=70, blank=True, verbose_name='Email пользователя')
    comments_text = models.TextField(verbose_name='Текст сообщения')
    comments_article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.comments_text

    def clean(self):
        if self.login_user == '':
            self.login_user = None
        if self.email_user == '':
            self.email_user = None
