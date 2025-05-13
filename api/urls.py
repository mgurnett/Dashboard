from django.urls import path
from . import views

urlpatterns = [
    path("", views.getData, name="getData"),
    path("add/", views.addReading, name="postData"),
    path("status/", views.addStatus, name="postStatus"),
]