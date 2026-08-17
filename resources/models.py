from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class DocumentResource(models.Model):
    """
    Documento institucional reutilizable en una o varias
    acciones de formación de la misma institución.
    """

    DOCUMENT_TYPE_CHOICES = [
        ("PROTOCOL", "Protocolo"),
        ("CLINICAL_GUIDE", "Guía de práctica clínica"),
        ("PROCEDURE", "Procedimiento"),
        ("MANUAL", "Manual"),
        ("INSTRUCTION", "Instructivo"),
        ("FORMAT", "Formato"),
        ("RESOLUTION", "Resolución"),
        ("OTHER", "Otro"),
    ]

    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.PROTECT,
        related_name="document_resources",
        verbose_name="Institución",
    )

    title = models.CharField(
        max_length=250,
        verbose_name="Título",
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Tipo de documento",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    file = models.FileField(
        upload_to="resources/documents/",
        verbose_name="Archivo",
    )

    version = models.CharField(
        max_length=30,
        default="1.0",
        verbose_name="Versión",
    )

    document_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha del documento",
    )

    training_actions = models.ManyToManyField(
        "training.TrainingAction",
        related_name="document_resources",
        blank=True,
        verbose_name="Acciones de formación",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_document_resources",
        verbose_name="Creado por",
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
        verbose_name = "Documento institucional"
        verbose_name_plural = "Biblioteca documental"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - v{self.version}"

    def clean(self):
        super().clean()

        if self.pk:
            invalid_actions = self.training_actions.exclude(
                institution=self.institution
            )

            if invalid_actions.exists():
                raise ValidationError(
                    {
                        "training_actions": (
                            "Todos los documentos deben asociarse únicamente "
                            "a capacitaciones de la misma institución."
                        )
                    }
                )


class MediaResource(models.Model):
    """
    Recurso multimedia institucional reutilizable en una o varias
    acciones de formación de la misma institución.
    """

    MEDIA_TYPE_CHOICES = [
        ("VIDEO", "Video"),
        ("PRESENTATION", "Presentación"),
        ("AUDIO", "Audio"),
        ("IMAGE", "Imagen"),
        ("INFOGRAPHIC", "Infografía"),
        ("LINK", "Enlace"),
        ("OTHER", "Otro"),
    ]

    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.PROTECT,
        related_name="media_resources",
        verbose_name="Institución",
    )

    title = models.CharField(
        max_length=250,
        verbose_name="Título",
    )

    media_type = models.CharField(
        max_length=30,
        choices=MEDIA_TYPE_CHOICES,
        verbose_name="Tipo de recurso",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    file = models.FileField(
        upload_to="resources/media/",
        blank=True,
        null=True,
        verbose_name="Archivo",
    )

    external_url = models.URLField(
        blank=True,
        verbose_name="Enlace externo",
    )

    training_actions = models.ManyToManyField(
        "training.TrainingAction",
        related_name="media_resources",
        blank=True,
        verbose_name="Acciones de formación",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_media_resources",
        verbose_name="Creado por",
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
        verbose_name = "Recurso multimedia"
        verbose_name_plural = "Biblioteca multimedia"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if not self.file and not self.external_url:
            raise ValidationError(
                "Debe proporcionar un archivo o un enlace externo."
            )

        if self.pk:
            invalid_actions = self.training_actions.exclude(
                institution=self.institution
            )

            if invalid_actions.exists():
                raise ValidationError(
                    {
                        "training_actions": (
                            "Los recursos multimedia solo pueden asociarse "
                            "a capacitaciones de la misma institución."
                        )
                    }
                )