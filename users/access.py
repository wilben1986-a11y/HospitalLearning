from django.core.exceptions import PermissionDenied

from .models import InstitutionalLink


def get_active_institutional_link(user):
    """
    Devuelve la primera vinculación institucional activa del usuario.

    Esta función centraliza la selección de la IPS activa para que,
    cuando HospitalLearning incorpore selección explícita de IPS,
    la lógica pueda modificarse en un único lugar.
    """
    return (
        InstitutionalLink.objects.filter(
            user=user,
            active=True,
        )
        .select_related("institution")
        .order_by("id")
        .first()
    )


def get_active_institution(user):
    """
    Devuelve la institución activa del usuario o None.
    """
    link = get_active_institutional_link(user)

    if link is None:
        return None

    return link.institution


def require_institution_admin(request):
    """
    Exige que el usuario sea administrador y tenga
    una vinculación institucional activa.

    Devuelve la institución activa.
    """
    if not (
        request.user.is_staff
        or request.user.is_superuser
    ):
        raise PermissionDenied(
            "No tienes permisos de administración institucional."
        )

    institution = get_active_institution(request.user)

    if institution is None:
        raise PermissionDenied(
            "No tienes una institución activa asociada."
        )

    return institution


def require_institution_admin_with_link(request):
    """
    Igual que require_institution_admin(), pero devuelve
    tanto la institución como la vinculación institucional.

    Se utiliza en módulos que necesitan ambos objetos,
    como reportes.
    """
    if not (
        request.user.is_staff
        or request.user.is_superuser
    ):
        raise PermissionDenied(
            "No tienes permisos de administración institucional."
        )

    link = get_active_institutional_link(request.user)

    if link is None:
        raise PermissionDenied(
            "No tienes una institución activa asociada."
        )

    return link.institution, link