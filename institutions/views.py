from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from training.models import ActionType
from users.access import require_institution_admin

from .forms import ActionTypeForm, InstitutionForm, ServiceForm
from .models import Service


@login_required
def settings_view(request):
    institution = require_institution_admin(request)

    return render(
        request,
        "institutions/settings.html",
        {
            "institution": institution,
            "action_types": ActionType.objects.filter(
                institution=institution
            ).order_by("name"),
            "services": Service.objects.filter(
                institution=institution
            )
            .select_related("parent")
            .order_by("name"),
        },
    )


@login_required
def institution_edit(request):
    institution = require_institution_admin(request)

    form = InstitutionForm(
        request.POST or None,
        instance=institution,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "La información institucional fue actualizada correctamente.",
        )

        return redirect("institutions_ui:settings")

    return render(
        request,
        "institutions/institution_form.html",
        {
            "institution": institution,
            "form": form,
        },
    )


@login_required
def service_create(request):
    institution = require_institution_admin(request)

    form = ServiceForm(
        request.POST or None,
        institution=institution,
    )

    if request.method == "POST" and form.is_valid():
        service = form.save(commit=False)
        service.institution = institution
        service.full_clean()
        service.save()

        messages.success(
            request,
            "Servicio creado correctamente.",
        )

        return redirect("institutions_ui:settings")

    return render(
        request,
        "institutions/service_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Nuevo servicio",
        },
    )


@login_required
def service_edit(request, pk):
    institution = require_institution_admin(request)

    service = get_object_or_404(
        Service,
        pk=pk,
        institution=institution,
    )

    form = ServiceForm(
        request.POST or None,
        instance=service,
        institution=institution,
    )

    if request.method == "POST" and form.is_valid():
        service = form.save(commit=False)
        service.institution = institution
        service.full_clean()
        service.save()

        messages.success(
            request,
            "Servicio actualizado correctamente.",
        )

        return redirect("institutions_ui:settings")

    return render(
        request,
        "institutions/service_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Editar servicio",
            "service": service,
        },
    )


@login_required
def action_type_create(request):
    institution = require_institution_admin(request)

    form = ActionTypeForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():
        action_type = form.save(commit=False)
        action_type.institution = institution
        action_type.full_clean()
        action_type.save()

        messages.success(
            request,
            "Tipo de acción creado correctamente.",
        )

        return redirect("institutions_ui:settings")

    return render(
        request,
        "institutions/action_type_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Nuevo tipo de acción",
        },
    )


@login_required
def action_type_edit(request, pk):
    institution = require_institution_admin(request)

    action_type = get_object_or_404(
        ActionType,
        pk=pk,
        institution=institution,
    )

    form = ActionTypeForm(
        request.POST or None,
        instance=action_type,
    )

    if request.method == "POST" and form.is_valid():
        action_type = form.save(commit=False)
        action_type.institution = institution
        action_type.full_clean()
        action_type.save()

        messages.success(
            request,
            "Tipo de acción actualizado correctamente.",
        )

        return redirect("institutions_ui:settings")

    return render(
        request,
        "institutions/action_type_form.html",
        {
            "institution": institution,
            "form": form,
            "title": "Editar tipo de acción",
            "action_type": action_type,
        },
    )