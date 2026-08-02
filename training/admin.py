from django.contrib import admin

from .models import ActionType


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "institution",
        "active",
        "requires_certificate",
    )

    list_filter = (
        "institution",
        "active",
        "requires_certificate",
        "requires_renewal",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "institution",
        "name",
    )