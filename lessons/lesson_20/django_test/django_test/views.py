from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from articles.models import Article, Tag
import random
# Create your views here.
def home_page(request):
    random_idx = random.randint(0, Article.objects.count() - 1)
    # return HttpResponse('This is the home page')
    art_random = get_object_or_404(Article, id=random_idx+1)
    return render(request, 'articles/index.html',{'articles':art_random})
