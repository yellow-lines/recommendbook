from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Case, When
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from web.forms import NewUserForm
from web.models import Category, Article
from web.serializers import CategorySerializer, ArticleSerializer, UserSerializer
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
import pandas as pd

def index(request):
    query = request.GET.get('q')  # получение значения поиска
    print(query)
    if query != None:
        return render(request, 'web/list.html')
    return render(request, 'web/index.html')


# @login_required
def list(request):
    books = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'k', 10: 'l', 11: 'm'}

    # books = Books.objects.all()
    # query = request.GET.get('q')
    # if query:
    # books = Books.objects.filter(Q(title__icontains=query)).distinct()
    # return render(request, 'web/list.html', {'books': books})

    return render(request, 'web/list.html', books)


def reader_cab(request):
    return render(request, 'web/reader_cab.html')


def list(request):
    """engine = create_engine("postgresql://postgres:sleeperonelove@127.0.0.1:5432/recommender_users")
    connection = engine.connect()
    dr1 = pd.read_sql("SELECT * FROM adress_table", connection)"""



    server = SSHTunnelForwarder(
        ('217.28.238.125', 22),
        ssh_username="owner",
        ssh_password="здесь ваш закрытый ssh ключ",
        remote_bind_address=('127.0.0.1', 5432)
    )

    server.start()
    local_port = str(server.local_bind_port)
    engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format("postgres", "sleeperonelove", "127.0.0.1", local_port, "recommender_users"))
    connection = engine.connect()
    dr1 = pd.read_sql("select title from stockstats_cat", connection)
    print(dr1.loc[0])
    return render(request, 'web/list.html', )


def book(request):
    return render(request, 'web/book.html', )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("reader_cab")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="web/signup.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("reader_cab")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request, template_name="web/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")

def connect(request):
    engine = create_engine("postgresql://postgres:sleeperonelove@127.0.0.1:5432/recommender_users")
    connection = engine.connect()
    dr1 = pd.read_sql("SELECT * FROM adress_table", connection)
    return 0