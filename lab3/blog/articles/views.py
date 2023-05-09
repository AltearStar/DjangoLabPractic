from django.shortcuts import render
from django.http import HttpResponse
from articles.models import Article

# Create your views here.

def home(request):
    return render(request, 'index.html')

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})