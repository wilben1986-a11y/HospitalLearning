from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """
    Representa a una persona que puede estar vinculada
    a una o varias Instituciones Prestadoras de Servicios de Salud.
    """

    DOCUMENT_TYPE_CHOICES = [
        ("CC", "Cédula de ciudadanía"),
        ("CE", "Cédula de extranjería"),
        ("PA", "Pasaporte"),
        ("PEP", "Permiso Especial de Permanencia"),
        ("PPT", "Permiso por Protección Temporal"),
        ("OTRO", "Otro"),
    ]

    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Tipo de documento",
    )

    document_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Número de documento",
    )

    profession = models.CharField(
        max_length=150,
        verbose_name="Profesión",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username


class InstitutionalLink(models.Model):
    """
    Representa la vinculación actual de un usuario con una IPS.

    El usuario puede estar asociado a uno o varios servicios.
    Los cambios de servicio no eliminan su historial de formación.
    """

    ROLE_CHOICES = [
        ("ADMINISTRADOR", "Administrador"),
        ("INSTRUCTOR", "Instructor"),
        ("PARTICIPANTE", "Participante"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="institutional_links",
        verbose_name="Usuario",
    )

    institution = models.ForeignKey(
        "institutions.Institution",
        on_delete=models.PROTECT,
        related_name="user_links",
        verbose_name="Institución",
    )

    services = models.ManyToManyField(
        "institutions.Service",
        related_name="user_links",
        blank=True,
        verbose_name="Servicios",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="PARTICIPANTE",
        verbose_name="Rol en la plataforma",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Vinculación activa",
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
        verbose_name = "Vinculación institucional"
        verbose_name_plural = "Vinculaciones institucionales"
        ordering = ["institution", "user__last_name", "user__first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "institution"],
                name="unique_user_institution_link",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.institution}"