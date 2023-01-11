from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main_page(request):
    return HttpResponse('This is main page')

def article_description(request):
    return HttpResponse('This is some article')