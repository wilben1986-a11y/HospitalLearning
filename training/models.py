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
        "training.ActionType",
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

    def __str__(self):
        return f"{self.code} - {self.name} (v{self.version})"