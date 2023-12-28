from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorRating = models.SmallIntegerField(default=0)
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        postRat = 0
        postRat += post_rating.get('postRating')

        comm_rat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        commRat = 0
        commRat += comm_rat.get('commentRating')

        self.authorRating = postRat * 3 + commRat
        self.save()

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def get_category(self):
        return self.category

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = "NW"
    ARTICLE = "AR"
    CHOICES_CATEGORY =(
        (NEWS, "Новости"),
        (ARTICLE, "Статьи"),
    )
    category_type = models.CharField(max_length=2, choices=CHOICES_CATEGORY, default=ARTICLE)
    date_created = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')
        # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.heading.title()}: {self.text[:124]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{ self.postThrough.heading} | { self.categoryThrough.category}'


class Comment(models.Model):
    text = models.TextField()
    dataCreate = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription (models.Model):
    pass
