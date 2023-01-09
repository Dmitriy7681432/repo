from django.core.management.base import BaseCommand
from articles.models import Article,Tag

class Command(BaseCommand):

    def handle(self, *args, **options):

        #Запрос в базу без условия
        print('DB command')
        articles =Article.objects.all()
        print(type(articles),articles)
        for art in articles:
            print(art.article_text)

        #Запрос в базу c условия
        #get
        art_ = Article.objects.get(article_name = 'Happy loin')
        print(art_)