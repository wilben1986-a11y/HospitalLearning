from django.contrib import admin

from .models import DocumentResource, MediaResource


@admin.register(DocumentResource)
class DocumentResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "document_type",
        "institution",
        "version",
        "document_date",
        "active",
        "created_by",
        "updated_at",
    )

    list_filter = (
        "institution",
        "document_type",
        "active",
        "document_date",
    )

    search_fields = (
        "title",
        "description",
        "version",
        "institution__name",
    )

    filter_horizontal = (
        "training_actions",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "institution",
        "title",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "institution",
                    "title",
                    "document_type",
                    "description",
                )
            },
        ),
        (
            "Documento",
            {
                "fields": (
                    "file",
                    "version",
                    "document_date",
                )
            },
        ),
        (
            "Capacitaciones relacionadas",
            {
                "fields": (
                    "training_actions",
                )
            },
        ),
        (
            "Estado y auditoría",
            {
                "fields": (
                    "active",
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "media_type",
        "institution",
        "active",
        "created_by",
        "updated_at",
    )

    list_filter = (
        "institution",
        "media_type",
        "active",
    )

    search_fields = (
        "title",
        "description",
        "external_url",
        "institution__name",
    )

    filter_horizontal = (
        "training_actions",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "institution",
        "title",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "institution",
                    "title",
                    "media_type",
                    "description",
                )
            },
        ),
        (
            "Recurso multimedia",
            {
                "fields": (
                    "file",
                    "external_url",
                )
            },
        ),
        (
            "Capacitaciones relacionadas",
            {
                "fields": (
                    "training_actions",
                )
            },
        ),
        (
            "Estado y auditoría",
            {
                "fields": (
                    "active",
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )