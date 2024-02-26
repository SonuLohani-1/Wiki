from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:title>', views.view_title, name = "view_title"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random/", views.get_random, name="get_random")
]
