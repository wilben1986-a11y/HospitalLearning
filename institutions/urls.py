from django.urls import path

from . import views


app_name = "institutions_ui"

urlpatterns = [
    path("configuracion/", views.settings_view, name="settings"),
]