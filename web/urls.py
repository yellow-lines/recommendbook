from django.urls import path
from django.contrib.auth import views
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

#from web.views import UserViewSet, CategoryViewSet, ArticleViewSet
from . import views


"""router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet)"""

"""urlpatterns = [
    path('', include(router.urls)),
]"""
urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path('reader_cab/', views.reader_cab, name="reader_cab"),
    path('list/', views.list, name='list'),
    path('book/', views.book, name='book'),
]