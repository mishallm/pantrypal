from django.urls import path

from . import views

app_name = "pantry"

urlpatterns = [
    path("", views.item_list, name="list"),
    path("add/", views.item_create, name="create"),
    path("<int:pk>/edit/", views.item_update, name="update"),
    path("<int:pk>/delete/", views.item_delete, name="delete"),
    path("<int:pk>/finish/<str:outcome>/", views.item_finish, name="finish"),
]
