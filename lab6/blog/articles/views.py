from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from articles.models import Article
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

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

def create_accuont(request):
    if request.method == "POST":
        form = {
            'name': request.POST["name"], 'email': request.POST["email"], 'password': request.POST["password"]
        }
        if form["name"] and form["email"] and form["password"]:
            try:
                User.objects.get(username=form["name"])
                form['errors'] = u"Пользователь с таким именем уже есть"
                return render(request, 'create_account.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(form["name"], form["email"], form["password"])
                return redirect('Archive')

        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'create_account.html', {'form': form})
    else:
        return render(request, 'create_account.html', {})
        
def login_accuont(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'name': request.POST["name"], 'password': request.POST["password"]
            }
            if form["name"] and form["password"]:
                user = authenticate(username=form["name"], password=form["password"])
                if user:
                    login(request, user)
                    return redirect('Archive')
                else:
                    form['errors'] = u"Некорректные данные для входа"
                    return render(request, 'login_account.html', {'form': form})   
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login_account.html', {'form': form})
        else:
            return render(request, 'login_account.html', {})
    else:
        logout(request)
        return redirect('Archive')