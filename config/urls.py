"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "cuenta/",
        include("django.contrib.auth.urls"),
    ),

    path(
        "capacitaciones/",
        include("training.urls"),
    ),

    path(
        "usuarios/",
        include("users.urls"),
    ),

    path(
        "evaluaciones/",
        include("assessments.urls"),
    ),

    path(
        "certificados/",
        include("certificates.urls"),
    ),

    path(
        "institucion/",
        include("institutions.urls"),
    ),

    path(
        "reportes/",
        include("reports.urls"),
    ),

    path(
        "recursos/",
        include("resources.urls"),
    ),

    path("", include("pages.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )