from django.urls import path

from . import views


app_name = "training_ui"

urlpatterns = [
    path("gestion/", views.management, name="management"),
]