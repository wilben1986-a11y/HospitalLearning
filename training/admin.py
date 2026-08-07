from django.contrib import admin

from .models import (
    ActionType,
    TrainingAction,
    TrainingAssignment,
    TrainingResult,
)


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "institution",
        "active",
        "requires_certificate",
        "requires_renewal",
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
        "status",
        "mandatory",
        "active",
    )

    list_filter = (
        "institution",
        "action_type",
        "status",
        "mandatory",
        "active",
        "requires_pretest",
        "requires_final_evaluation",
        "generates_certificate",
    )

    search_fields = (
        "code",
        "name",
        "objective",
    )

    ordering = (
        "institution",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "institution",
                    "action_type",
                    "name",
                    "code",
                    "objective",
                    "description",
                )
            },
        ),
        (
            "Contenido de aprendizaje",
            {
                "fields": (
                    "learning_content",
                ),
                "description": (
                    "Cargue el archivo HTML principal de la capacitación."
                ),
            },
        ),
        (
            "Publicación",
            {
                "fields": (
                    "version",
                    "status",
                    "publication_date",
                    "mandatory",
                    "active",
                )
            },
        ),
        (
            "Configuración pedagógica",
            {
                "fields": (
                    "requires_pretest",
                    "requires_final_evaluation",
                    "requires_complete_content",
                    "passing_score",
                    "max_attempts",
                )
            },
        ),
        (
            "Certificación",
            {
                "fields": (
                    "generates_certificate",
                    "automatic_certificate",
                )
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(TrainingAssignment)
class TrainingAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "training_action",
        "user",
        "status",
        "assigned_by",
        "assigned_at",
        "due_date",
    )

    list_filter = (
        "status",
        "assigned_at",
        "training_action__institution",
    )

    search_fields = (
        "training_action__name",
        "training_action__code",
        "user__first_name",
        "user__last_name",
        "user__username",
    )

    ordering = (
        "-assigned_at",
    )

    readonly_fields = (
        "assigned_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Asignación",
            {
                "fields": (
                    "training_action",
                    "user",
                    "assigned_by",
                    "status",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "assigned_at",
                    "due_date",
                    "updated_at",
                )
            },
        ),
        (
            "Observaciones",
            {
                "fields": (
                    "observations",
                )
            },
        ),
    )


@admin.register(TrainingResult)
class TrainingResultAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "pretest_score",
        "posttest_score",
        "improvement_points",
        "approved",
        "attempt_number",
        "completed_at",
    )

    list_filter = (
        "approved",
        "attempt_number",
        "completed_at",
        "assignment__training_action__institution",
    )

    search_fields = (
        "assignment__training_action__name",
        "assignment__training_action__code",
        "assignment__user__first_name",
        "assignment__user__last_name",
        "assignment__user__username",
    )

    ordering = (
        "-completed_at",
    )

    readonly_fields = (
        "improvement_points",
        "completed_at",
    )

    fieldsets = (
        (
            "Resultado",
            {
                "fields": (
                    "assignment",
                    "pretest_score",
                    "posttest_score",
                    "improvement_points",
                    "approved",
                    "attempt_number",
                )
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "completed_at",
                )
            },
        ),
    )