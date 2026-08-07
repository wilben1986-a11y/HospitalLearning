from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "mis-capacitaciones/",
        views.my_trainings,
        name="my_trainings",
    ),

    path(
        "capacitacion/<int:pk>/",
        views.training_view,
        name="training_view",
    ),

    path(
        "capacitacion/<int:pk>/contenido/",
        views.training_content,
        name="training_content",
    ),

    path(
        "capacitacion/<int:pk>/resultado/",
        views.save_training_result,
        name="save_training_result",
    ),
]