from django.urls import path

from . import views


app_name = "training_ui"


urlpatterns = [
    path(
        "gestion/",
        views.management,
        name="management",
    ),
    path(
        "gestion/nueva/",
        views.training_create,
        name="training_create",
    ),
    path(
        "gestion/<int:pk>/editar/",
        views.training_edit,
        name="training_edit",
    ),
    path(
        "gestion/<int:pk>/asignar/",
        views.training_assign,
        name="training_assign",
    ),
]