from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Usuario personalizado de HospitalLearning.
    Representa a una persona que puede estar vinculada a una o varias IPS.
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