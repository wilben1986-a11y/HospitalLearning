from django.contrib import admin

from .models import ActionType, TrainingAction


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


@admin.register(TrainingAction)
class TrainingActionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "institution",
        "action_type",
        "version",
        "status",
    )

    list_filter = (
        "institution",
        "action_type",
        "status",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = (
        "institution",
        "name",
    )