from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("entries/<str:title>", views.entry, name="entry"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("deletepage/<str:title>", views.deletepage, name="deletepage")
]
