from django.urls import path,re_path
from . import views
from .views import *

urlpatterns = [
    path ('', views.Home.as_view(), name = 'home'),
]