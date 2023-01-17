# -*- coding: utf-8 -*-
from django import forms
from .models import Tag, Article

'''
class ArticleForm(forms.Form):
    name = forms.CharField(label='Название статьи', max_length=100)
    text = forms.CharField(label='Техт статьи')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple())
'''
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        #fields = ('article_name','article_text')
        # exclude = ('tags')
