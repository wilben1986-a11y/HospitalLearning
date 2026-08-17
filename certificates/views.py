from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from users.access import require_institution_admin

from .models import Certificate


@login_required
def management(request):
    institution = require_institution_admin(request)

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
        certificates = certificates.filter(
            active=(active == "yes")
        )
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