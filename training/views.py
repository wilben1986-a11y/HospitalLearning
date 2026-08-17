from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from users.access import require_institution_admin

from .forms import BulkTrainingAssignmentForm, TrainingActionForm
from .models import ActionType, TrainingAction, TrainingAssignment


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
        .prefetch_related("assignments")
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
        actions = actions.filter(status=status)
    else:
        status = ""

    if action_type:
        try:
            action_type_id = int(action_type)
        except (TypeError, ValueError):
            action_type = ""
        else:
            if action_types.filter(pk=action_type_id).exists():
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
            "status_choices": TrainingAction.STATUS_CHOICES,
            "q": q,
            "selected_status": status,
            "selected_action_type": action_type,
            "selected_active": active,
        },
    )


@login_required
def training_create(request):
    institution = require_institution_admin(request)

    if request.method == "POST":
        form = TrainingActionForm(
            request.POST,
            request.FILES,
            institution=institution,
        )

        if form.is_valid():
            training = form.save(commit=False)
            training.institution = institution
            training.created_by = request.user
            training.full_clean()
            training.save()

            messages.success(
                request,
                "Capacitación creada correctamente.",
            )

            return redirect("training_ui:management")

    else:
        form = TrainingActionForm(
            institution=institution,
        )

    return render(
        request,
        "training/training_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Nueva capacitación",
        },
    )


@login_required
def training_edit(request, pk):
    institution = require_institution_admin(request)

    training = get_object_or_404(
        TrainingAction,
        pk=pk,
        institution=institution,
    )

    if request.method == "POST":
        form = TrainingActionForm(
            request.POST,
            request.FILES,
            instance=training,
            institution=institution,
        )

        if form.is_valid():
            training = form.save(commit=False)
            training.institution = institution
            training.full_clean()
            training.save()

            messages.success(
                request,
                "Capacitación actualizada correctamente.",
            )

            return redirect("training_ui:management")

    else:
        form = TrainingActionForm(
            instance=training,
            institution=institution,
        )

    return render(
        request,
        "training/training_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Editar capacitación",
            "training": training,
        },
    )


@login_required
def training_assign(request, pk):
    institution = require_institution_admin(request)

    training = get_object_or_404(
        TrainingAction,
        pk=pk,
        institution=institution,
    )

    existing_assignments = (
        TrainingAssignment.objects.filter(
            training_action=training,
        )
        .select_related("user", "assigned_by")
        .order_by("user__last_name", "user__first_name", "user__username")
    )

    if request.method == "POST":
        form = BulkTrainingAssignmentForm(
            request.POST,
            institution=institution,
            training_action=training,
        )

        if form.is_valid():
            participants = form.cleaned_data["participants"]
            due_date = form.cleaned_data["due_date"]
            observations = form.cleaned_data["observations"]

            created_count = 0

            for participant in participants:
                assignment = TrainingAssignment(
                    training_action=training,
                    user=participant,
                    assigned_by=request.user,
                    due_date=due_date,
                    observations=observations,
                )
                assignment.full_clean()
                assignment.save()
                created_count += 1

            messages.success(
                request,
                f"Se asignó la capacitación a {created_count} participante(s).",
            )

            return redirect(
                "training_ui:training_assign",
                pk=training.pk,
            )

    else:
        form = BulkTrainingAssignmentForm(
            institution=institution,
            training_action=training,
        )

    return render(
        request,
        "training/training_assign.html",
        {
            "institution": institution,
            "training": training,
            "form": form,
            "existing_assignments": existing_assignments,
        },
    )