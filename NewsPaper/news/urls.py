from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, ARCreate, ARUpdate, ARDelete,
   subscriptions, CategoryListView,
)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='posts_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('articles/create/', ARCreate.as_view(), name='ar_create'),
   path('articles/<int:pk>/update/', ARUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', ARDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   # path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]
