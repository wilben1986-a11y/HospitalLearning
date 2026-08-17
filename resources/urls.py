from django.urls import path

from . import views


app_name = "resources_ui"


urlpatterns = [
    path(
        "documentos/",
        views.document_library,
        name="document_library",
    ),
    path(
        "documentos/nuevo/",
        views.document_create,
        name="document_create",
    ),
    path(
        "documentos/<int:pk>/editar/",
        views.document_edit,
        name="document_edit",
    ),
    path(
        "multimedia/",
        views.media_library,
        name="media_library",
    ),
    path(
        "multimedia/nuevo/",
        views.media_create,
        name="media_create",
    ),
    path(
        "multimedia/<int:pk>/editar/",
        views.media_edit,
        name="media_edit",
    ),
]