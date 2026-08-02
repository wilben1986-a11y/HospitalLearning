from django.db import models


class Institution(models.Model):
    """
    Representa una Institución Prestadora de Servicios de Salud (IPS)
    dentro de HospitalLearning.
    """

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )

    nit = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Número de Identificación Tributaria (NIT)"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
        ordering = ["name"]

    def __str__(self):
        return self.name