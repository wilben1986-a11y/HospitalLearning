from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .access import require_institution_admin
from .models import InstitutionalLink


@login_required
def management(request):
    institution = require_institution_admin(request)

    links = (
        InstitutionalLink.objects.filter(
            institution=institution
        )
        .select_related(
            "user",
            "institution",
        )
        .prefetch_related("services")
        .order_by(
            "user__last_name",
            "user__first_name",
            "user__username",
        )
    )

    q = (request.GET.get("q") or "").strip()
    profession = (
        request.GET.get("profession") or ""
    ).strip()
    link_status = (
        request.GET.get("link_status") or ""
    ).strip()

    professions = list(
        links.exclude(
            user__profession=""
        )
        .values_list(
            "user__profession",
            flat=True,
        )
        .distinct()
        .order_by("user__profession")
    )

    if q:
        links = links.filter(
            Q(user__username__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(user__document_number__icontains=q)
            | Q(user__email__icontains=q)
        )

    if profession:
        if profession in professions:
            links = links.filter(
                user__profession=profession
            )
        else:
            profession = ""

    if link_status in {"active", "inactive"}:
        links = links.filter(
            active=(link_status == "active")
        )
    else:
        link_status = ""

    return render(
        request,
        "users/management.html",
        {
            "institution": institution,
            "links": links,
            "professions": professions,
            "q": q,
            "selected_profession": profession,
            "selected_link_status": link_status,
        },
    )