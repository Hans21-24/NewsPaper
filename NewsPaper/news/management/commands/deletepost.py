from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление статей из выбранной категории'

    def add_argument(self, parser):
        parser.add_argument("category", type=str, help='Введите название категории.')

    def handle(self, *args, **options):
        answer = input(f'Вы хотите удалить все статьи из категории {options["category"]}? yes/no:   ')

        if answer == 'yes':
            try:
                category = Category.objects.get(category=options['category'])
                post = Post.objects.filter(postCategory=category)
                post.delete()
                self.stdout.write(self.style.SUCCESS(f'Все статьи из категории {category.category} удалены!'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Категория {category.category} не найдена.'))
        else:
            self.stdout.write(self.style.ERROR(f'Удаление отменено.'))
