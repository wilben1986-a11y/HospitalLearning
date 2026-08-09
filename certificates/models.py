import uuid

from django.core.exceptions import ValidationError
from django.db import models


class Certificate(models.Model):
    """
    Representa el certificado emitido a un participante
    por una capacitación aprobada.
    """

    assignment = models.OneToOneField(
        "training.TrainingAssignment",
        on_delete=models.PROTECT,
        related_name="certificate",
        verbose_name="Asignación",
    )

    verification_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Código de verificación",
    )

    issued_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de emisión",
    )

    active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    observations = models.TextField(
        blank=True,
        verbose_name="Observaciones",
    )

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        ordering = ["-issued_at"]

    def clean(self):
        """
        Valida que el certificado solo pueda emitirse
        para una capacitación finalizada y aprobada.
        """

        if not self.assignment_id:
            return

        training = self.assignment.training_action

        if not training.generates_certificate:
            raise ValidationError(
                {
                    "assignment": (
                        "Esta capacitación no está configurada "
                        "para generar certificado."
                    )
                }
            )

        try:
            result = self.assignment.result
        except Exception:
            raise ValidationError(
                {
                    "assignment": (
                        "La asignación todavía no tiene "
                        "un resultado de capacitación."
                    )
                }
            )

        if result.completed_at is None:
            raise ValidationError(
                {
                    "assignment": (
                        "La capacitación todavía no ha sido finalizada."
                    )
                }
            )

        if not result.approved:
            raise ValidationError(
                {
                    "assignment": (
                        "Solo se puede generar certificado "
                        "para una capacitación aprobada."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Certificado - "
            f"{self.assignment.user} - "
            f"{self.assignment.training_action.name}"
        )