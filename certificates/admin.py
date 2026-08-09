from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "participant",
        "training",
        "issued_at",
        "active",
        "verification_code",
    )

    list_filter = (
        "active",
        "issued_at",
    )

    search_fields = (
        "assignment__user__username",
        "assignment__user__first_name",
        "assignment__user__last_name",
        "assignment__training_action__name",
        "verification_code",
    )

    readonly_fields = (
        "verification_code",
        "issued_at",
    )

    ordering = (
        "-issued_at",
    )

    @admin.display(description="Participante")
    def participant(self, obj):
        return obj.assignment.user

    @admin.display(description="Capacitación")
    def training(self, obj):
        return obj.assignment.training_action