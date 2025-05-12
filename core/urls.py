from django.urls import path,re_path
from . import views
from .views import *

urlpatterns = [
    path ('', views.Home.as_view(), name = 'home'),
    path ('main/', views.Main.as_view(), name = 'main'),
    path ('chain/<int:pk>/', views.ChainList.as_view(), name = 'chain_detail'),
]