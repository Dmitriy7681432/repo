from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Tag

# Create your views here.
def main_page(request):
    art_all = Article.objects.all()
    # return HttpResponse(f'number of articles {len(art_all)}')
    # return render(request, 'articles/articles_main.html', {'articles': art_all})
    return render(request, 'articles/category.html', {'articles': art_all})
def article_description(request, id):
    # art_one = Article.objects.first()
    # return HttpResponse(f'Text: {art_one.article_text}')
    art_one = get_object_or_404(Article, id =id)
    return render(request, 'articles/single.html', {'article': art_one})
