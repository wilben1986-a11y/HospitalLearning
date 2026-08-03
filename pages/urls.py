from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

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
]