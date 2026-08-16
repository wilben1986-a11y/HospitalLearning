from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from training.models import TrainingResult
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
def management(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    institution = _active_institution_for(request.user)
    if institution is None:
        raise PermissionDenied("No tienes una institución activa asociada.")

    results = (
        TrainingResult.objects.filter(
            assignment__training_action__institution=institution
        )
        .select_related(
            "assignment",
            "assignment__user",
            "assignment__training_action",
        )
        .order_by("-completed_at", "assignment__user__last_name")
    )

    q = (request.GET.get("q") or "").strip()
    approved = (request.GET.get("approved") or "").strip()

    if q:
        results = results.filter(
            Q(assignment__user__username__icontains=q)
            | Q(assignment__user__first_name__icontains=q)
            | Q(assignment__user__last_name__icontains=q)
            | Q(assignment__training_action__name__icontains=q)
            | Q(assignment__training_action__code__icontains=q)
        )

    if approved in {"yes", "no"}:
        results = results.filter(approved=(approved == "yes"))
    else:
        approved = ""

    return render(
        request,
        "assessments/management.html",
        {
            "institution": institution,
            "results": results,
            "q": q,
            "selected_approved": approved,
        },
    )