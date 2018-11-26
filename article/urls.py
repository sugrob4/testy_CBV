from django.urls import path, re_path

from article.views import Home, SecondeHome, Spisok


urlpatterns = [
    path('', Home.as_view(), name='article'),
    path('home/', SecondeHome.as_view(), name='secondehome'),
    path('home/add_like/<int:pk>', SecondeHome.as_view(), name='add_like'),
    path('home/<int:pk>-<slug:browser_url>', Spisok.as_view(), name='spisok'),
    path('add_comment/<int:pk>', Spisok.as_view(), name='add_comment'),
    re_path('home/page=([\d]+)$', SecondeHome.as_view()),
]
