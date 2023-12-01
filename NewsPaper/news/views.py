from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views.decorators.csrf import csrf_protect
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import PostFilter
from .models import Post, Category
from .forms import PostForm


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = ['-date_created']
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'



# Добавляем новое представление для создания товаров.
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель новостей
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = "NW"
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление удаляющее товар.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class ARCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель новостей
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = "AR"
        return super().form_valid(form)


class ARUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ARDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


# class CategoryListView(ListView):
#     model = Post
#     template_name = 'category_list.html'
#     context_object_name = 'category_news_list'
#     ordering = ['-date_created']
#     paginate_by = 10
#
#     def get_queryset(self):
#         self.id = resolve(self.request.path_info).kwargs['pk']
#         category = Category.objects.get(id=self.id)
#         queryset = Post.objects.filter(postCategory=category)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(*kwargs)
#         user = self.request.user
#         category = Category.objects.get(id=self.id)
#         subscribed = category.subscribers.filter(email=user.email)
#         if not subscribed:
#             context['category'] = category
#
#         return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['is_subscriber'] = self.request.user in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context

@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'postCategory': category, 'message': message})

@login_required
@csrf_protect
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Подписка отменена'
    return render(request, 'unsubscribe.html', {'postCategory': category, 'message': message})

# @login_required
# @csrf_protect
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#
#     if not category.subscribers.filter(id=user.id).exists():
#         category.subscribers.add(user)
#         email = user.email
#         html = render_to_string(
#             'subscribe.html',
#             {
#                 'category': category,
#                 'user': user,
#             }
#         )
#         msg = EmailMultiAlternatives(
#             subject=f'{category} subscription',
#             body='',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[email,],
#         )
#         msg.attach_alternative(html, 'text/html')
#
#         try:
#             msg.send()
#         except Exception as e:
#             print(e)
#         message = 'Вы успешно подписались на рассылку новостей категории'
#         return redirect(request, 'subscribe.html', {'postCategory': category, 'message': message})
#     return redirect(request.META.get('HTTP_REFERER'))
#
# @login_required
# @csrf_protect
# def unsubscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#
#     if category.subscribers.filter(id=user.id).exists():
#         category.subscribers.remove(user)
#         message = 'Подписка отменена'
#     return redirect(request, 'unsubscribe.html', {'postCategory': category, 'message': message})

# @login_required
# @csrf_protect
# def subscriptions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')
#
#         if action == 'subscribe':
#             Subscription.objects.create(user=request.user, category=category)
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=category,
#             ).delete()
#
#     categories_with_subscriptions = Category.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=OuterRef('pk'),
#             )
#         )
#     ).order_by('category')
#     return render(
#         request,
#         'subscriptions.html',
#         {'categories': categories_with_subscriptions},
#     )
