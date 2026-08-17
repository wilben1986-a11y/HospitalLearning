from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from users.access import require_institution_admin

from .models import ActionType, TrainingAction


@login_required
def management(request):
    institution = require_institution_admin(request)

    actions = (
        TrainingAction.objects.filter(
            institution=institution
        )
        .select_related(
            "action_type",
            "created_by",
        )
        .order_by("name")
    )

    action_types = ActionType.objects.filter(
        institution=institution,
        active=True,
    ).order_by("name")

    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "").strip()
    action_type = (
        request.GET.get("action_type") or ""
    ).strip()
    active = (request.GET.get("active") or "").strip()

    if q:
        actions = actions.filter(
            Q(name__icontains=q)
            | Q(code__icontains=q)
            | Q(objective__icontains=q)
        )

    valid_statuses = {
        value
        for value, _label
        in TrainingAction.STATUS_CHOICES
    }

    if status in valid_statuses:
        actions = actions.filter(
            status=status
        )
    else:
        status = ""

    if action_type:
        try:
            action_type_id = int(action_type)
        except ValueError:
            action_type = ""
        else:
            if action_types.filter(
                pk=action_type_id
            ).exists():
                actions = actions.filter(
                    action_type_id=action_type_id
                )
            else:
                action_type = ""

    if active in {"yes", "no"}:
        actions = actions.filter(
            active=(active == "yes")
        )
    else:
        active = ""

    return render(
        request,
        "training/management.html",
        {
            "institution": institution,
            "actions": actions,
            "action_types": action_types,
            "status_choices": (
                TrainingAction.STATUS_CHOICES
            ),
            "q": q,
            "selected_status": status,
            "selected_action_type": action_type,
            "selected_active": active,
        },
    )