from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from users.models import InstitutionalLink

from .forms import DocumentResourceForm, MediaResourceForm
from .models import DocumentResource, MediaResource


def _active_institution_for(user):
    link = (
        InstitutionalLink.objects.filter(
            user=user,
            active=True,
        )
        .select_related("institution")
        .order_by("id")
        .first()
    )

    return link.institution if link else None


def _require_admin_institution(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    institution = _active_institution_for(request.user)

    if institution is None:
        raise PermissionDenied(
            "No tienes una institución activa asociada."
        )

    return institution


@login_required
def document_library(request):
    institution = _require_admin_institution(request)

    documents = (
        DocumentResource.objects.filter(
            institution=institution,
        )
        .select_related(
            "created_by",
            "institution",
        )
        .prefetch_related("training_actions")
        .order_by("title")
    )

    q = (request.GET.get("q") or "").strip()
    document_type = (request.GET.get("document_type") or "").strip()
    active = (request.GET.get("active") or "").strip()

    if q:
        documents = documents.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(version__icontains=q)
            | Q(training_actions__name__icontains=q)
            | Q(training_actions__code__icontains=q)
        ).distinct()

    valid_types = {
        value
        for value, _label in DocumentResource.DOCUMENT_TYPE_CHOICES
    }

    if document_type in valid_types:
        documents = documents.filter(document_type=document_type)
    else:
        document_type = ""

    if active in {"yes", "no"}:
        documents = documents.filter(active=(active == "yes"))
    else:
        active = ""

    return render(
        request,
        "resources/document_library.html",
        {
            "institution": institution,
            "documents": documents,
            "document_type_choices": (
                DocumentResource.DOCUMENT_TYPE_CHOICES
            ),
            "q": q,
            "selected_document_type": document_type,
            "selected_active": active,
        },
    )


@login_required
def document_create(request):
    institution = _require_admin_institution(request)

    if request.method == "POST":
        form = DocumentResourceForm(
            request.POST,
            request.FILES,
            institution=institution,
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.institution = institution
            document.created_by = request.user
            document.full_clean()
            document.save()
            form.save_m2m()

            messages.success(
                request,
                "Documento institucional creado correctamente.",
            )

            return redirect("resources_ui:document_library")

    else:
        form = DocumentResourceForm(
            institution=institution,
        )

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "institution": institution,
            "title": "Nuevo documento",
            "library_name": "Biblioteca documental",
            "back_url_name": "resources_ui:document_library",
        },
    )


@login_required
def document_edit(request, pk):
    institution = _require_admin_institution(request)

    document = get_object_or_404(
        DocumentResource,
        pk=pk,
        institution=institution,
    )

    if request.method == "POST":
        form = DocumentResourceForm(
            request.POST,
            request.FILES,
            instance=document,
            institution=institution,
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.institution = institution
            document.full_clean()
            document.save()
            form.save_m2m()

            messages.success(
                request,
                "Documento institucional actualizado correctamente.",
            )

            return redirect("resources_ui:document_library")

    else:
        form = DocumentResourceForm(
            instance=document,
            institution=institution,
        )

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "institution": institution,
            "title": "Editar documento",
            "library_name": "Biblioteca documental",
            "back_url_name": "resources_ui:document_library",
        },
    )


@login_required
def media_library(request):
    institution = _require_admin_institution(request)

    resources = (
        MediaResource.objects.filter(
            institution=institution,
        )
        .select_related(
            "created_by",
            "institution",
        )
        .prefetch_related("training_actions")
        .order_by("title")
    )

    q = (request.GET.get("q") or "").strip()
    media_type = (request.GET.get("media_type") or "").strip()
    active = (request.GET.get("active") or "").strip()

    if q:
        resources = resources.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(external_url__icontains=q)
            | Q(training_actions__name__icontains=q)
            | Q(training_actions__code__icontains=q)
        ).distinct()

    valid_types = {
        value
        for value, _label in MediaResource.MEDIA_TYPE_CHOICES
    }

    if media_type in valid_types:
        resources = resources.filter(media_type=media_type)
    else:
        media_type = ""

    if active in {"yes", "no"}:
        resources = resources.filter(active=(active == "yes"))
    else:
        active = ""

    return render(
        request,
        "resources/media_library.html",
        {
            "institution": institution,
            "resources": resources,
            "media_type_choices": MediaResource.MEDIA_TYPE_CHOICES,
            "q": q,
            "selected_media_type": media_type,
            "selected_active": active,
        },
    )


@login_required
def media_create(request):
    institution = _require_admin_institution(request)

    if request.method == "POST":
        form = MediaResourceForm(
            request.POST,
            request.FILES,
            institution=institution,
        )

        if form.is_valid():
            media = form.save(commit=False)
            media.institution = institution
            media.created_by = request.user
            media.full_clean()
            media.save()
            form.save_m2m()

            messages.success(
                request,
                "Recurso multimedia creado correctamente.",
            )

            return redirect("resources_ui:media_library")

    else:
        form = MediaResourceForm(
            institution=institution,
        )

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "institution": institution,
            "title": "Nuevo recurso multimedia",
            "library_name": "Biblioteca multimedia",
            "back_url_name": "resources_ui:media_library",
        },
    )


@login_required
def media_edit(request, pk):
    institution = _require_admin_institution(request)

    media = get_object_or_404(
        MediaResource,
        pk=pk,
        institution=institution,
    )

    if request.method == "POST":
        form = MediaResourceForm(
            request.POST,
            request.FILES,
            instance=media,
            institution=institution,
        )

        if form.is_valid():
            media = form.save(commit=False)
            media.institution = institution
            media.full_clean()
            media.save()
            form.save_m2m()

            messages.success(
                request,
                "Recurso multimedia actualizado correctamente.",
            )

            return redirect("resources_ui:media_library")

    else:
        form = MediaResourceForm(
            instance=media,
            institution=institution,
        )

    return render(
        request,
        "resources/resource_form.html",
        {
            "form": form,
            "institution": institution,
            "title": "Editar recurso multimedia",
            "library_name": "Biblioteca multimedia",
            "back_url_name": "resources_ui:media_library",
        },
    )