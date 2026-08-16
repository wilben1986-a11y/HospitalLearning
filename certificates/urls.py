from django.urls import path

from . import views


app_name = "certificates_ui"

urlpatterns = [
    path("gestion/", views.management, name="management"),
]