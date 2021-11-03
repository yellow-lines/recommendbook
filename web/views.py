from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
import sqlalchemy
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm  # add this
from web.forms import NewUserForm
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
        print(query.split())
        aut_ = '"aut"'
        title_ = '"title"'
        sql_request = f"select * from stockstats_cat where({title_} ilike '%{query}%' or {aut_} ilike '%{query}%')"
        dr2 = pd.read_sql(sqlalchemy.text(sql_request), connection)
        search_output = dr2.reset_index().to_json(orient='records')
        search_data = []
        search_data = json.loads(search_output)
        return render(request, 'web/list.html', context={'content': search_data})
    return render(request, 'web/index.html')


def book(request):
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
    id_book = str(request.GET.get('recId'))
    if id_book != None:
        dep_books = get_dep_books(id_book, connection)
        output = dep_books.reset_index().to_json(orient='records')
        data = []
        data = json.loads(output)

    # dict_keys(['index', 'recId', 'aut', 'title', 'place', 'publ', 'yea', 'lan', 'rubrics', 'serial'])
    return render(request, 'web/book.html', context={'content': data})


def reader_cab(request):
    history_data = get_history_data(request.user.username, connection)
    history_output = history_data.reset_index().to_json(orient='records')
    history_data = []
    history_data = json.loads(history_output)
    request.session['history_data'] = history_data

    recommend_data = get_id_exp1(request.user.username, connection)
    recommend_output = recommend_data.reset_index().to_json(orient='records')
    recommend_data = []
    recommend_data = json.loads(recommend_output)
    request.session['recommend_data'] = recommend_data

    query = request.GET.get('q')
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
    return render(request, 'web/reader_cab.html', context={'content': history_data})



def list(request):

    recommend_data = get_id_exp1(request.user.username, connection)
    output = recommend_data.reset_index().to_json(orient='records')
    data = []
    data = json.loads(output)

    query = request.GET.get('q')  
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

def download_json(request):
    recommend_data = request.session.get('recommend_data')
    history_data = request.session.get('history_data')
    download_data = dict_transform(recommend_data, history_data)
    response = HttpResponse(download_data, content_type="application/json")
    #response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response

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


def graph_request(request):

    got_net = Network(height='100%',
                      width='100%',
                      bgcolor='#222222',
                      font_color='white',
                      notebook=True)

    got_net.barnes_hut()

    username = request.user.username
    got_data, exp_person = get_id_exp2(username, connection)

    sources = got_data['Object_1']
    targets = got_data['Object_2']
    weights = got_data['Weight']
    src_title = got_data['Source']
    trg_title = got_data['Target']

    edge_data = zip(sources, targets, weights, src_title, trg_title)

    for e in edge_data:
        src = e[3]
        dst = e[4]
        w = e[2]
        src_ttl = e[0]
        dst_ttl = e[1]
        if src_ttl in exp_person:
            clr = 'yellow'
            shp = 'diamond'
        else:
            clr = '#D2E5FF'
            shp = 'dot'
        if dst_ttl in exp_person:
            clr2 = 'yellow'
            shp2 = 'diamond'
        else:
            clr2 = '#D2E5FF'
            shp2 = 'dot'

        got_net.add_node(src, src, color=clr, shape=shp, title=src)
        got_net.add_node(dst, dst, color=clr2, shape=shp2, title=dst)
        got_net.add_edge(src, dst, value=w, color='#D2E5FF')

    neighbor_map = got_net.get_adj_list()
    # добавить данные о соседях в узлы
    for node in got_net.nodes:
        node['title'] += ' Связи:<br>' + \
            '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])
    got_net.show('templates/graph.html')

    return render(request, template_name="graph.html")
