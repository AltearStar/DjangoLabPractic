from django.shortcuts import render
from django.http import HttpResponse
from articles.models import Article
from django.http import Http404

# Create your views here.

def home(request):
    return render(request, 'index.html')

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})
    
def get_article(request, article_id = 1):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404
