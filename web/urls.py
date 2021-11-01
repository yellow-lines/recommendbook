from django.urls import path
from django.contrib.auth import views
from django.urls import path
from django.conf.urls import url, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path('reader_cab/', views.reader_cab, name="reader_cab"),
    path('list/', views.list, name='list'),
    url(r'^book/$', views.book, name='book'),
    url('graph/', views.graph_request, name='graph')
]
