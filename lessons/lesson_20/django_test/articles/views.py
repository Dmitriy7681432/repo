# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Article, Tag
from .forms import ArticleForm
import datetime

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

def article_add(request):
    if request.method =="GET":
        form = ArticleForm()
        return render(request, 'articles/article_add.html', {'form': form})
    else:
        # Первый случай
        # form =ArticleForm(request.POST)
        #Второй случай
        form = ArticleForm(request.POST, files=request.FILES)
        if form.is_valid():
            #Обработка данных
            '''
            #В первом случае создании формы
            name =form.cleaned_data['name']
            text =form.cleaned_data['text']
            tags =form.cleaned_data['tags']
            print(f'{name},{text},{tags}')
            article_object = Article(article_name = name, article_text = text, article_data = datetime.now(),article_img=ImageFile(open('media/articles/happy_lion.jpg','rb')))
            article_object.save()
            '''
            #Во втором случае создании формы
            form.save()
            # Article.objects.create(article_name = name, article_text = text, article_tag =tags)
            return HttpResponseRedirect(reverse('articles:index'))
        else:
            return render(request, 'articles/article_add.html', {'form': form})
