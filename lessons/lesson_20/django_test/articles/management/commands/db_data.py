from django.core.management.base import BaseCommand
# from repo.lessons.lesson_20.django_test.articles.models import Article,Tag
from repo.lessons.lesson_20.django_test.articles.models import Article
class Command(BaseCommand):

    def handle(self, *args, **options):

        print('DB command')
        articles =Article.objects.all()
        print(type(articles),articles)