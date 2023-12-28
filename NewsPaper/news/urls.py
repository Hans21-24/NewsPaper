from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, ARCreate, ARUpdate, ARDelete,
   subscribe, CategoryListView, unsubscribe,
)
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
   path('articles/create/', ARCreate.as_view(), name='ar_create'),
   path('articles/<int:pk>/update/', ARUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', ARDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
   # path('subscriptions/', subscriptions, name='subscriptions'),
]
