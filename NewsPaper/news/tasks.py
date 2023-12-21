import datetime
from celery import shared_task
from django.conf import settings
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def weekly_send_emails():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_created__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'registration/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Посты за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'registration/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()