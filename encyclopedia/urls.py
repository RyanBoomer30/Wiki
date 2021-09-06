from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("create", views.create, name="create"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("edit", views.edit, name="edit"),
    path("shuffle", views.shuffle, name="shuffle")
]
