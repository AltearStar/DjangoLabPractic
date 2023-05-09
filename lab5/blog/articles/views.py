from django.shortcuts import render
from django.shortcuts import redirect
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

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                if not Article.objects.filter(title = form["title"]).exists():
                    # если заголовок не существует
                    obj = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', obj.id)
                    # перейти на страницу поста
                else:
                    form['errors'] = u"Статья с таким названием уже существует"
                    return render(request, 'create_post.html', {'form': form})
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404

