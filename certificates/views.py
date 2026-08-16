from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from users.models import InstitutionalLink
from .models import Certificate


def _active_institution_for(user):
    link = (
        InstitutionalLink.objects.filter(user=user, active=True)
        .select_related("institution")
        .order_by("id")
        .first()
    )
    return link.institution if link else None


@login_required
def management(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    institution = _active_institution_for(request.user)
    if institution is None:
        raise PermissionDenied("No tienes una institución activa asociada.")

    certificates = (
        Certificate.objects.filter(
            assignment__training_action__institution=institution
        )
        .select_related(
            "assignment",
            "assignment__user",
            "assignment__training_action",
        )
        .order_by("-issued_at")
    )

    q = (request.GET.get("q") or "").strip()
    active = (request.GET.get("active") or "").strip()

    if q:
        certificates = certificates.filter(
            Q(assignment__user__username__icontains=q)
            | Q(assignment__user__first_name__icontains=q)
            | Q(assignment__user__last_name__icontains=q)
            | Q(assignment__training_action__name__icontains=q)
            | Q(assignment__training_action__code__icontains=q)
            | Q(verification_code__icontains=q)
        )

    if active in {"yes", "no"}:
        certificates = certificates.filter(active=(active == "yes"))
    else:
        active = ""

    return render(
        request,
        "certificates/management.html",
        {
            "institution": institution,
            "certificates": certificates,
            "q": q,
            "selected_active": active,
        },
    )