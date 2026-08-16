from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from training.models import ActionType
from users.models import InstitutionalLink


def _active_institution_for(user):
    link = (
        InstitutionalLink.objects.filter(user=user, active=True)
        .select_related("institution")
        .order_by("id")
        .first()
    )
    return link.institution if link else None


@login_required
def settings_view(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    institution = _active_institution_for(request.user)
    if institution is None:
        raise PermissionDenied("No tienes una institución activa asociada.")

    action_types = ActionType.objects.filter(
        institution=institution
    ).order_by("name")

    services = institution.services.select_related("parent").order_by("name")

    return render(
        request,
        "institutions/settings.html",
        {
            "institution": institution,
            "action_types": action_types,
            "services": services,
        },
    )