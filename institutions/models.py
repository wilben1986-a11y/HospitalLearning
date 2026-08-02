from django.db import models
from django.core.exceptions import ValidationError

class Institution(models.Model):
    """
    Representa una Institución Prestadora de Servicios de Salud (IPS)
    dentro de HospitalLearning.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre",
    )

    nit = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Número de Identificación Tributaria (NIT)",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa",
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
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Representa un servicio asistencial disponible en una IPS.

    Cada institución puede configurar sus propios servicios.
    """

    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name="Institución",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subservices",
        blank=True,
        null=True,
        verbose_name="Servicio principal",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Nombre del servicio",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
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
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["institution", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "name"],
                name="unique_service_name_per_institution",
            )
        ]

def clean(self):
    if self.parent and self.parent.institution_id != self.institution_id:
        raise ValidationError(
            {
                "parent": (
                    "El servicio principal debe pertenecer "
                    "a la misma institución."
                )
            }
        )
        
    def __str__(self):
        return f"{self.name} - {self.institution}"