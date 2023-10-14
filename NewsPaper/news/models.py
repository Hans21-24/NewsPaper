from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


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


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = "NW"
    ARTICLE = "AR"
    CHOICES_CATEGORY =(
        (NEWS, "Новость"),
        (ARTICLE, "Статья"),
    )
    category_type = models.CharField(max_length=2, choices=CHOICES_CATEGORY, default=ARTICLE)
    date_created = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


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