from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from training.models import TrainingResult
from users.access import require_institution_admin


@login_required
def management(request):
    institution = require_institution_admin(request)

    results = (
        TrainingResult.objects.filter(
            assignment__training_action__institution=institution
        )
        .select_related(
            "assignment",
            "assignment__user",
            "assignment__training_action",
        )
        .order_by(
            "-completed_at",
            "assignment__user__last_name",
        )
    )

    q = (request.GET.get("q") or "").strip()
    approved = (
        request.GET.get("approved") or ""
    ).strip()

    if q:
        results = results.filter(
            Q(
                assignment__user__username__icontains=q
            )
            | Q(
                assignment__user__first_name__icontains=q
            )
            | Q(
                assignment__user__last_name__icontains=q
            )
            | Q(
                assignment__training_action__name__icontains=q
            )
            | Q(
                assignment__training_action__code__icontains=q
            )
        )

    if approved in {"yes", "no"}:
        results = results.filter(
            approved=(approved == "yes")
        )
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