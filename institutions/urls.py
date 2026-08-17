from django.urls import path
from . import views
app_name="institutions_ui"
urlpatterns=[
    path("configuracion/",views.settings_view,name="settings"),
    path("configuracion/institucion/editar/",views.institution_edit,name="institution_edit"),
    path("configuracion/servicios/nuevo/",views.service_create,name="service_create"),
    path("configuracion/servicios/<int:pk>/editar/",views.service_edit,name="service_edit"),
    path("configuracion/tipos-accion/nuevo/",views.action_type_create,name="action_type_create"),
    path("configuracion/tipos-accion/<int:pk>/editar/",views.action_type_edit,name="action_type_edit"),
]