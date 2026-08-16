from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from .models import InstitutionalLink


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

    links = (
        InstitutionalLink.objects.filter(institution=institution)
        .select_related("user", "institution")
        .prefetch_related("services")
        .order_by("user__last_name", "user__first_name", "user__username")
    )

    q = (request.GET.get("q") or "").strip()
    profession = (request.GET.get("profession") or "").strip()
    link_status = (request.GET.get("link_status") or "").strip()

    professions = list(
        links.exclude(user__profession="")
        .values_list("user__profession", flat=True)
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
            links = links.filter(user__profession=profession)
        else:
            profession = ""

    if link_status in {"active", "inactive"}:
        links = links.filter(active=(link_status == "active"))
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