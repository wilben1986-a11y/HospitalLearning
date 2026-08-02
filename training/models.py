from django.core.exceptions import ValidationError
from django.db import models


class ActionType(models.Model):
    """
    Clasifica las acciones de formación de una institución
    y define sus reglas generales de cumplimiento.
    """

    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.PROTECT,
        related_name="action_types",
        verbose_name="Institución",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Nombre",
    )

    code = models.CharField(
        max_length=30,
        verbose_name="Código",
    )

    objective = models.TextField(
        verbose_name="Objetivo",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    requires_certificate = models.BooleanField(
        default=True,
        verbose_name="Requiere certificado",
    )

    has_validity = models.BooleanField(
        default=False,
        verbose_name="Tiene vigencia",
    )

    requires_renewal = models.BooleanField(
        default=False,
        verbose_name="Requiere renovación periódica",
    )

    renewal_period_months = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Período de renovación en meses",
    )

    new_version_requires_retake = models.BooleanField(
        default=False,
        verbose_name="Nueva versión obliga a repetir la formación",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Tipo de acción"
        verbose_name_plural = "Tipos de acción"
        ordering = ["institution", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "name"],
                name="unique_action_type_name_per_institution",
            ),
            models.UniqueConstraint(
                fields=["institution", "code"],
                name="unique_action_type_code_per_institution",
            ),
        ]

    def clean(self):
        if self.requires_renewal and not self.renewal_period_months:
            raise ValidationError(
                {
                    "renewal_period_months": (
                        "Debe indicar el período de renovación cuando "
                        "el tipo requiera renovación periódica."
                    )
                }
            )

        if not self.requires_renewal:
            self.renewal_period_months = None

    def __str__(self):
        return f"{self.code} - {self.name}"


class TrainingAction(models.Model):
    """
    Representa una acción de formación creada por una institución.
    """

    STATUS_CHOICES = [
        ("DRAFT", "Borrador"),
        ("PUBLISHED", "Publicada"),
        ("ARCHIVED", "Archivada"),
    ]

    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.PROTECT,
        related_name="training_actions",
        verbose_name="Institución",
    )

    action_type = models.ForeignKey(
        ActionType,
        on_delete=models.PROTECT,
        related_name="training_actions",
        verbose_name="Tipo de acción",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre",
    )

    code = models.CharField(
        max_length=30,
        verbose_name="Código",
    )

    objective = models.TextField(
        verbose_name="Objetivo",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    version = models.CharField(
        max_length=20,
        default="1.0",
        verbose_name="Versión",
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="DRAFT",
        verbose_name="Estado",
    )

    created_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.PROTECT,
        related_name="training_actions_created",
        verbose_name="Responsable de la creación",
    )

    publication_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de publicación",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    mandatory = models.BooleanField(
        default=True,
        verbose_name="Obligatoria",
    )

    requires_pretest = models.BooleanField(
        default=False,
        verbose_name="Requiere pretest",
    )

    requires_final_evaluation = models.BooleanField(
        default=False,
        verbose_name="Requiere evaluación final",
    )

    requires_complete_content = models.BooleanField(
        default=True,
        verbose_name="Requiere completar todo el contenido",
    )

    passing_score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Puntaje mínimo de aprobación",
    )

    max_attempts = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Número máximo de intentos",
    )

    generates_certificate = models.BooleanField(
        default=False,
        verbose_name="Genera certificado",
    )

    automatic_certificate = models.BooleanField(
        default=False,
        verbose_name="Emisión automática del certificado",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Acción de formación"
        verbose_name_plural = "Acciones de formación"
        ordering = ["institution", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"],
                name="unique_training_action_code_per_institution",
            ),
        ]

    def clean(self):
        if self.action_type_id and self.institution_id:
            if self.action_type.institution_id != self.institution_id:
                raise ValidationError(
                    {
                        "action_type": (
                            "El Tipo de Acción debe pertenecer "
                            "a la misma institución."
                        )
                    }
                )

        if self.requires_final_evaluation and self.passing_score is None:
            raise ValidationError(
                {
                    "passing_score": (
                        "Debe indicar el puntaje mínimo cuando la capacitación "
                        "requiera evaluación final."
                    )
                }
            )

        if self.passing_score is not None and self.passing_score > 100:
            raise ValidationError(
                {
                    "passing_score": (
                        "El puntaje mínimo de aprobación no puede superar 100."
                    )
                }
            )

        if self.max_attempts is not None and self.max_attempts < 1:
            raise ValidationError(
                {
                    "max_attempts": (
                        "El número máximo de intentos debe ser mayor que cero."
                    )
                }
            )

        if not self.requires_final_evaluation:
            self.passing_score = None
            self.max_attempts = None

        if not self.generates_certificate:
            self.automatic_certificate = False

    def __str__(self):
        return f"{self.code} - {self.name} (v{self.version})"


class TrainingAssignment(models.Model):
    """
    Representa la asignación de una Acción de Formación
    a un usuario específico.
    """

    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("IN_PROGRESS", "En progreso"),
        ("APPROVED", "Aprobada"),
        ("NOT_APPROVED", "No aprobada"),
        ("EXPIRED", "Vencida"),
    ]

    training_action = models.ForeignKey(
        TrainingAction,
        on_delete=models.PROTECT,
        related_name="assignments",
        verbose_name="Acción de formación",
    )

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.PROTECT,
        related_name="training_assignments",
        verbose_name="Usuario",
    )

    assigned_by = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.PROTECT,
        related_name="training_assignments_created",
        verbose_name="Responsable de la asignación",
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de asignación",
    )

    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha límite",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
        verbose_name="Estado",
    )

    observations = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Asignación de capacitación"
        verbose_name_plural = "Asignaciones de capacitación"
        ordering = ["-assigned_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["training_action", "user"],
                name="unique_training_action_assignment_per_user",
            ),
        ]

    def clean(self):
        if self.training_action_id:
            if not self.training_action.active:
                raise ValidationError(
                    {
                        "training_action": (
                            "Solo se pueden asignar capacitaciones activas."
                        )
                    }
                )

            if self.training_action.status != "PUBLISHED":
                raise ValidationError(
                    {
                        "training_action": (
                            "Solo se pueden asignar capacitaciones publicadas."
                        )
                    }
                )

        if self.due_date and self.assigned_at:
            if self.due_date < self.assigned_at.date():
                raise ValidationError(
                    {
                        "due_date": (
                            "La fecha límite no puede ser anterior "
                            "a la fecha de asignación."
                        )
                    }
                )

    def __str__(self):
        return f"{self.training_action} - {self.user}"