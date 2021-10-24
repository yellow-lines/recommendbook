from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
import sqlalchemy
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
import json
from web.recommendations import *
from pyvis.network import Network



server = SSHTunnelForwarder(
        ('178.154.241.46', 22),
        ssh_username="owner",
        ssh_password="здесь ваш закрытый ssh ключ",
        remote_bind_address=('127.0.0.1', 5432)
    )

server.start()
local_port = str(server.local_bind_port)
engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format("postgres", "sleeperonelove", "127.0.0.1", local_port,
                                             "recommender_users"))
connection = engine.connect()

def index(request):
    query = request.GET.get('q')  # получение значения поиска
    if query != None:
        return ('book', query)
    return render(request, 'web/index.html')

def book(request):
    dr1 = pd.read_sql("select * from stockstats_cat limit 50", connection)
    output = dr1.reset_index().to_json(orient='records')
    data = []
    data = json.loads(output)

    query = request.GET.get('q')  # получение значения поиска
    if query != None:
        print(query.split())
        aut_ = '"aut"'
        title_ = '"title"'
        sql_request = f"select * from stockstats_cat where({title_} ilike '%{query}%' or {aut_} ilike '%{query}%')"
        dr2 = pd.read_sql(sqlalchemy.text(sql_request), connection)
        search_output = dr2.reset_index().to_json(orient='records')
        search_data = []
        search_data = json.loads(search_output)
        return render(request, 'web/list.html', context={'content': search_data})


    # dict_keys(['index', 'recId', 'aut', 'title', 'place', 'publ', 'yea', 'lan', 'rubrics', 'serial'])
    return render(request, 'web/book.html', context={'content': data})


def reader_cab(request):

    dr1 = pd.read_sql("select * from stockstats_cat limit 50", connection)
    dr_search = dr1
    output = dr1.reset_index().to_json(orient='records')
    data = []
    data = json.loads(output)
    query = request.GET.get('q')  # получение значения поиска
    if query != None:
        print(query.split())
        aut_ = '"aut"'
        title_ = '"title"'
        sql_request = f"select * from stockstats_cat where({title_} ilike '%{query}%' or {aut_} ilike '%{query}%')"
        dr2 = pd.read_sql(sqlalchemy.text(sql_request), connection)
        search_output = dr2.reset_index().to_json(orient='records')
        search_data = []
        search_data = json.loads(search_output)
        return render(request, 'web/list.html', context={'content': search_data})

        return render(request, 'web/list.html', context={'content': data})
    # dict_keys(['index', 'recId', 'aut', 'title', 'place', 'publ', 'yea', 'lan', 'rubrics', 'serial'])
    return render(request, 'web/reader_cab.html', context={'content': data})


def list(request):
    """engine = create_engine("postgresql://postgres:sleeperonelove@127.0.0.1:5432/recommender_users")
    connection = engine.connect()
    dr1 = pd.read_sql("SELECT * FROM adress_table", connection)"""


    """dr1 = pd.read_sql("select * from stockstats_cat limit 50", connection)
    output = dr1.reset_index().to_json(orient='records')
    data = []
    data = json.loads(output)"""

    recommend_data = get_id_exp1('login_313414', connection)
    output = recommend_data.reset_index().to_json(orient='records')
    data = []
    data = json.loads(output)

    query = request.GET.get('q')  # получение значения поиска
    if query != None:
        print(query.split())
        aut_ = '"aut"'
        title_ = '"title"'
        sql_request = f"select * from stockstats_cat where({title_} ilike '%{query}%' or {aut_} ilike '%{query}%')"
        dr2 = pd.read_sql(sqlalchemy.text(sql_request), connection)
        search_output = dr2.reset_index().to_json(orient='records')
        search_data = []
        search_data = json.loads(search_output)
        return render(request, 'web/list.html', context={'content': search_data})

    return render(request, 'web/list.html', context={'content': data})


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
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
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
                messages.info(request, f"Вы вошли как {username}.")
                return redirect("reader_cab")
            else:
                messages.error(request, "Неверный пароль или логин.")
        else:
            messages.error(request, "Неверный пароль или логин.")

    form = AuthenticationForm()
    return render(request=request, template_name="web/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


def connect(request):
    engine = create_engine(
        "postgresql://postgres:sleeperonelove@127.0.0.1:5432/recommender_users")
    connection = engine.connect()
    dr1 = pd.read_sql("SELECT * FROM adress_table", connection)
    return 0


def graph_request(request):

    got_net = Network(height='100%',
                      width='100%',
                      bgcolor='#ffffff',
                      font_color='black',
                      notebook=False)

    # установить физический макет сети
    # https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.barnes_hut
    got_net.barnes_hut()
    got_data = pd.read_csv(
        'https://www.macalester.edu/~abeverid/data/stormofswords.csv')
    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w)

    # https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.get_adj_list
    neighbor_map = got_net.get_adj_list()

    # добавить данные о соседях в узлы
    for node in got_net.nodes:
        node['title'] += ' Neighbors:<br>' + \
            '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])

    got_net.show('templates/web/graph.html')

    return render(request=request, template_name="web/graph.html")

