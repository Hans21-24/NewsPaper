from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date_created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT',
            attrs={'type': 'date'},
        ),
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
           # поиск по названию
           'heading': ['icontains'],
           # поиск по категории
           'postCategory': ['exact'],
           # дата создания позже указанной даты
           # 'date_created': ['lt'],
       }