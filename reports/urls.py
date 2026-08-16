from django.urls import path

from . import views


app_name = "reports"


urlpatterns = [
    path(
        "",
        views.institutional_reports,
        name="institutional",
    ),
    path(
        "exportar/csv/<str:report_type>/",
        views.export_csv,
        name="export_csv",
    ),
    path(
        "exportar/pdf/",
        views.export_pdf,
        name="export_pdf",
    ),
]