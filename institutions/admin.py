from django.contrib import admin
from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nit",
        "code",
        "active",
    )

    search_fields = (
        "name",
        "nit",
        "code",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
    )