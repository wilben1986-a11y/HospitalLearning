import json
from io import BytesIO
from pathlib import Path

from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_http_methods, require_POST

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from certificates.models import Certificate
from users.models import CustomUser, InstitutionalLink
from training.models import (
    ActionType,
    TrainingAction,
    TrainingAssignment,
    TrainingResult,
)


@login_required
def home(request):
    """
    Página inicial de HospitalLearning.

    - Administradores y usuarios staff:
      Dashboard institucional filtrado por la IPS activa.
    - Participantes:
      Dashboard personal con sus propias capacitaciones,
      resultados y certificados.
    """

    # ==================================================
    # DASHBOARD INSTITUCIONAL
    # ==================================================

    if request.user.is_staff or request.user.is_superuser:

        institutional_link = (
            InstitutionalLink.objects.filter(
                user=request.user,
                active=True,
            )
            .select_related("institution")
            .order_by("id")
            .first()
        )

        institution = (
            institutional_link.institution
            if institutional_link is not None
            else None
        )

        if institution is not None:
            available_training_actions = (
                TrainingAction.objects.filter(
                    institution=institution,
                    active=True,
                )
                .select_related("action_type")
                .order_by("name")
            )

            available_action_types = (
                ActionType.objects.filter(
                    training_actions__institution=institution,
                    training_actions__active=True,
                )
                .distinct()
                .order_by("name")
            )

            available_professions = list(
                InstitutionalLink.objects.filter(
                    institution=institution,
                    active=True,
                )
                .exclude(user__profession="")
                .values_list("user__profession", flat=True)
                .distinct()
                .order_by("user__profession")
            )

            available_participants = (
                CustomUser.objects.filter(
                    training_assignments__training_action__institution=institution,
                )
                .distinct()
                .order_by("last_name", "first_name", "username")
            )

            available_statuses = list(
                TrainingAssignment._meta.get_field(
                    "status"
                ).choices
            )

            selected_training_action_id = request.GET.get(
                "training_action",
                "",
            ).strip()

            selected_action_type_id = request.GET.get(
                "action_type",
                "",
            ).strip()

            selected_profession = request.GET.get(
                "profession",
                "",
            ).strip()

            selected_status = request.GET.get("status", "").strip()
            selected_date_from = request.GET.get("date_from", "").strip()
            selected_date_to = request.GET.get("date_to", "").strip()
            selected_participant_id = request.GET.get("participant", "").strip()
            selected_mandatory = request.GET.get("mandatory", "").strip()
            selected_generates_certificate = request.GET.get(
                "generates_certificate", ""
            ).strip()

            selected_training_action = None
            selected_participant = None
            selected_action_type = None

            assignments = TrainingAssignment.objects.filter(
                training_action__institution=institution,
            )

            if selected_date_from:
                try:
                    date_from = date.fromisoformat(selected_date_from)
                except ValueError:
                    selected_date_from = ""
                else:
                    assignments = assignments.filter(
                        assigned_at__date__gte=date_from
                    )

            if selected_date_to:
                try:
                    date_to = date.fromisoformat(selected_date_to)
                except ValueError:
                    selected_date_to = ""
                else:
                    assignments = assignments.filter(
                        assigned_at__date__lte=date_to
                    )

            if selected_participant_id:
                try:
                    selected_participant = available_participants.get(
                        pk=selected_participant_id
                    )
                except (CustomUser.DoesNotExist, ValueError, TypeError):
                    selected_participant_id = ""
                    selected_participant = None
                else:
                    assignments = assignments.filter(user=selected_participant)

            if selected_mandatory in {"yes", "no"}:
                assignments = assignments.filter(
                    training_action__mandatory=(selected_mandatory == "yes")
                )
            else:
                selected_mandatory = ""

            if selected_generates_certificate in {"yes", "no"}:
                assignments = assignments.filter(
                    training_action__generates_certificate=(
                        selected_generates_certificate == "yes"
                    )
                )
            else:
                selected_generates_certificate = ""

            if selected_profession:
                if selected_profession not in available_professions:
                    selected_profession = ""
                else:
                    assignments = assignments.filter(
                        user__profession=selected_profession,
                    )

            valid_status_values = {
                value
                for value, _label in available_statuses
            }

            if selected_status:
                if selected_status not in valid_status_values:
                    selected_status = ""
                else:
                    assignments = assignments.filter(
                        status=selected_status,
                    )

            if selected_action_type_id:
                try:
                    selected_action_type = (
                        available_action_types.get(
                            pk=selected_action_type_id,
                        )
                    )
                except (
                    ActionType.DoesNotExist,
                    ValueError,
                    TypeError,
                ):
                    selected_action_type_id = ""
                    selected_action_type = None
                else:
                    assignments = assignments.filter(
                        training_action__action_type=selected_action_type,
                    )

            if selected_training_action_id:
                try:
                    selected_training_action = (
                        available_training_actions.get(
                            pk=selected_training_action_id,
                        )
                    )
                except (
                    TrainingAction.DoesNotExist,
                    ValueError,
                    TypeError,
                ):
                    selected_training_action_id = ""
                    selected_training_action = None
                else:
                    assignments = assignments.filter(
                        training_action=selected_training_action,
                    )

        else:
            available_training_actions = TrainingAction.objects.none()
            available_action_types = ActionType.objects.none()
            available_professions = []
            available_participants = CustomUser.objects.none()
            available_statuses = []
            selected_training_action_id = ""
            selected_action_type_id = ""
            selected_profession = ""
            selected_status = ""
            selected_date_from = ""
            selected_date_to = ""
            selected_participant_id = ""
            selected_mandatory = ""
            selected_generates_certificate = ""
            selected_training_action = None
            selected_action_type = None
            selected_participant = None
            assignments = TrainingAssignment.objects.none()

        total_participants = (
            assignments.values("user_id")
            .distinct()
            .count()
        )

        total_assignments = assignments.count()

        pending_assignments = assignments.filter(
            status="PENDING",
        ).count()

        in_progress_assignments = assignments.filter(
            status="IN_PROGRESS",
        ).count()

        approved_assignments = assignments.filter(
            status="APPROVED",
        ).count()

        not_approved_assignments = assignments.filter(
            status="NOT_APPROVED",
        ).count()

        completed_assignments = (
            approved_assignments + not_approved_assignments
        )

        if total_assignments > 0:
            compliance_percentage = round(
                (completed_assignments / total_assignments) * 100,
                1,
            )
        else:
            compliance_percentage = 0

        institutional_results = TrainingResult.objects.filter(
            assignment__in=assignments,
        )

        institutional_pretest_average = institutional_results.filter(
            pretest_score__isnull=False,
        ).aggregate(
            average=Avg("pretest_score"),
        )["average"]

        institutional_posttest_average = institutional_results.filter(
            posttest_score__isnull=False,
        ).aggregate(
            average=Avg("posttest_score"),
        )["average"]

        institutional_improvement_average = institutional_results.filter(
            pretest_score__isnull=False,
            posttest_score__isnull=False,
        ).aggregate(
            average=Avg("improvement_points"),
        )["average"]

        if institutional_pretest_average is not None:
            institutional_pretest_average = round(
                institutional_pretest_average,
                1,
            )

        if institutional_posttest_average is not None:
            institutional_posttest_average = round(
                institutional_posttest_average,
                1,
            )

        if institutional_improvement_average is not None:
            institutional_improvement_average = round(
                institutional_improvement_average,
                1,
            )

        certificates_issued = Certificate.objects.filter(
            assignment__in=assignments,
            active=True,
        ).count()

        training_actions = available_training_actions

        if selected_action_type is not None:
            training_actions = training_actions.filter(
                action_type=selected_action_type,
            )

        if selected_training_action is not None:
            training_actions = training_actions.filter(
                pk=selected_training_action.pk,
            )

        training_summary = []

        for training_action in training_actions:

            action_assignments = assignments.filter(
                training_action=training_action,
            )

            action_total = action_assignments.count()
            action_pending = action_assignments.filter(status="PENDING").count()
            action_in_progress = action_assignments.filter(status="IN_PROGRESS").count()
            action_approved = action_assignments.filter(status="APPROVED").count()
            action_not_approved = action_assignments.filter(status="NOT_APPROVED").count()
            action_completed = action_approved + action_not_approved

            if action_total > 0:
                action_compliance = round(
                    (action_completed / action_total) * 100,
                    1,
                )
            else:
                action_compliance = 0

            action_posttest_average = (
                TrainingResult.objects.filter(
                    assignment__in=action_assignments,
                    posttest_score__isnull=False,
                )
                .aggregate(
                    average=Avg("posttest_score"),
                )["average"]
            )

            if action_posttest_average is not None:
                action_posttest_average = round(
                    action_posttest_average,
                    1,
                )

            action_certificates = Certificate.objects.filter(
                assignment__in=action_assignments,
                active=True,
            ).count()

            training_summary.append(
                {
                    "training_action": training_action,
                    "assigned": action_total,
                    "pending": action_pending,
                    "in_progress": action_in_progress,
                    "completed": action_completed,
                    "approved": action_approved,
                    "not_approved": action_not_approved,
                    "compliance": action_compliance,
                    "posttest_average": action_posttest_average,
                    "certificates": action_certificates,
                }
            )

        participant_ids = (
            assignments.values_list("user_id", flat=True)
            .distinct()
        )

        participant_links = (
            InstitutionalLink.objects.filter(
                institution=institution,
                active=True,
                user_id__in=participant_ids,
            )
            .select_related("user")
            .order_by(
                "user__first_name",
                "user__last_name",
                "user__username",
            )
        )

        participant_summary = []

        for participant_link in participant_links:

            participant = participant_link.user

            participant_assignments = assignments.filter(
                user=participant,
            )

            participant_total = participant_assignments.count()

            participant_pending = participant_assignments.filter(
                status="PENDING",
            ).count()

            participant_in_progress = participant_assignments.filter(
                status="IN_PROGRESS",
            ).count()

            participant_approved = participant_assignments.filter(
                status="APPROVED",
            ).count()

            participant_not_approved = participant_assignments.filter(
                status="NOT_APPROVED",
            ).count()

            participant_completed = (
                participant_approved
                + participant_not_approved
            )

            if participant_total > 0:
                participant_compliance = round(
                    (
                        participant_completed
                        / participant_total
                    )
                    * 100,
                    1,
                )
            else:
                participant_compliance = 0

            participant_posttest_average = (
                TrainingResult.objects.filter(
                    assignment__in=participant_assignments,
                    posttest_score__isnull=False,
                )
                .aggregate(
                    average=Avg("posttest_score"),
                )["average"]
            )

            if participant_posttest_average is not None:
                participant_posttest_average = round(
                    participant_posttest_average,
                    1,
                )

            participant_certificates = (
                Certificate.objects.filter(
                    assignment__in=participant_assignments,
                    active=True,
                ).count()
            )

            participant_name = (
                participant.get_full_name().strip()
                or participant.username
            )

            document = "—"

            if participant.document_number:
                if participant.document_type:
                    document = (
                        f"{participant.document_type} "
                        f"{participant.document_number}"
                    )
                else:
                    document = participant.document_number

            profession = participant.profession or "—"

            participant_summary.append(
                {
                    "name": participant_name,
                    "username": participant.username,
                    "document": document,
                    "profession": profession,
                    "is_administrative": (
                        participant.is_staff
                        or participant.is_superuser
                    ),
                    "assigned": participant_total,
                    "pending": participant_pending,
                    "in_progress": participant_in_progress,
                    "completed": participant_completed,
                    "approved": participant_approved,
                    "not_approved": participant_not_approved,
                    "compliance": participant_compliance,
                    "posttest_average": participant_posttest_average,
                    "certificates": participant_certificates,
                }
            )

        context = {
            "dashboard_type": "institutional",
            "institution": institution,
            "institutional_link": institutional_link,
            "total_participants": total_participants,
            "total_assignments": total_assignments,
            "completed_assignments": completed_assignments,
            "compliance_percentage": compliance_percentage,
            "pending_assignments": pending_assignments,
            "in_progress_assignments": in_progress_assignments,
            "approved_assignments": approved_assignments,
            "not_approved_assignments": not_approved_assignments,
            "institutional_pretest_average": institutional_pretest_average,
            "institutional_posttest_average": institutional_posttest_average,
            "institutional_improvement_average": institutional_improvement_average,
            "certificates_issued": certificates_issued,
            "training_summary": training_summary,
            "participant_summary": participant_summary,
            "available_training_actions": available_training_actions,
            "available_action_types": available_action_types,
            "available_professions": available_professions,
            "available_participants": available_participants,
            "available_statuses": available_statuses,
            "selected_training_action_id": selected_training_action_id,
            "selected_training_action": selected_training_action,
            "selected_action_type_id": selected_action_type_id,
            "selected_action_type": selected_action_type,
            "selected_profession": selected_profession,
            "selected_status": selected_status,
            "selected_date_from": selected_date_from,
            "selected_date_to": selected_date_to,
            "selected_participant_id": selected_participant_id,
            "selected_participant": selected_participant,
            "selected_mandatory": selected_mandatory,
            "selected_generates_certificate": selected_generates_certificate,
        }

        return render(
            request,
            "pages/home.html",
            context,
        )

    # ==================================================
    # DASHBOARD PERSONAL DEL PARTICIPANTE
    # ==================================================

    assignments = TrainingAssignment.objects.filter(
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    )

    total_assignments = assignments.count()

    pending_assignments = assignments.filter(
        status="PENDING",
    ).count()

    in_progress_assignments = assignments.filter(
        status="IN_PROGRESS",
    ).count()

    approved_assignments = assignments.filter(
        status="APPROVED",
    ).count()

    not_approved_assignments = assignments.filter(
        status="NOT_APPROVED",
    ).count()

    completed_assignments = (
        approved_assignments + not_approved_assignments
    )

    results = TrainingResult.objects.filter(
        assignment__user=request.user,
    )

    pretest_average = results.filter(
        pretest_score__isnull=False,
    ).aggregate(
        average=Avg("pretest_score"),
    )["average"]

    posttest_average = results.filter(
        posttest_score__isnull=False,
    ).aggregate(
        average=Avg("posttest_score"),
    )["average"]

    improvement_average = results.filter(
        pretest_score__isnull=False,
        posttest_score__isnull=False,
    ).aggregate(
        average=Avg("improvement_points"),
    )["average"]

    if pretest_average is not None:
        pretest_average = round(pretest_average, 1)

    if posttest_average is not None:
        posttest_average = round(posttest_average, 1)

    if improvement_average is not None:
        improvement_average = round(improvement_average, 1)

    certificates_qs = (
        Certificate.objects.filter(
            assignment__user=request.user,
            active=True,
        )
        .select_related(
            "assignment",
            "assignment__training_action",
        )
        .order_by("-issued_at")
    )

    certificates_count = certificates_qs.count()

    next_assignments = (
        assignments.filter(
            status__in=[
                "PENDING",
                "IN_PROGRESS",
            ],
        )
        .select_related(
            "training_action",
        )
        .order_by(
            "due_date",
            "-assigned_at",
        )[:5]
    )

    recent_completed = list(
        assignments.filter(
            status__in=[
                "APPROVED",
                "NOT_APPROVED",
            ],
        )
        .select_related(
            "training_action",
        )
        .order_by(
            "-updated_at",
        )[:5]
    )

    for assignment in recent_completed:
        try:
            assignment.dashboard_result = assignment.result
        except TrainingResult.DoesNotExist:
            assignment.dashboard_result = None

    recent_completed.sort(
        key=lambda assignment: (
            assignment.dashboard_result.completed_at
            if (
                assignment.dashboard_result is not None
                and assignment.dashboard_result.completed_at is not None
            )
            else assignment.updated_at
        ),
        reverse=True,
    )

    recent_certificates = certificates_qs[:5]

    context = {
        "dashboard_type": "participant",
        "total_assignments": total_assignments,
        "pending_assignments": pending_assignments,
        "in_progress_assignments": in_progress_assignments,
        "completed_assignments": completed_assignments,
        "approved_assignments": approved_assignments,
        "not_approved_assignments": not_approved_assignments,
        "pretest_average": pretest_average,
        "posttest_average": posttest_average,
        "improvement_average": improvement_average,
        "certificates_count": certificates_count,
        "next_assignments": next_assignments,
        "recent_completed": recent_completed,
        "recent_certificates": recent_certificates,
    }

    return render(
        request,
        "pages/home.html",
        context,
    )

@login_required
def my_trainings(request):
    """
    Muestra las capacitaciones asignadas al usuario autenticado,
    separadas entre pendientes y realizadas.
    """

    assignments = (
        TrainingAssignment.objects.filter(
            user=request.user,
            training_action__active=True,
            training_action__status="PUBLISHED",
        )
        .select_related(
            "training_action",
            "training_action__action_type",
            "training_action__institution",
            "result",
        )
        .order_by("-assigned_at")
    )

    pending_assignments = assignments.filter(
        status__in=[
            "PENDING",
            "IN_PROGRESS",
        ]
    )

    completed_assignments = assignments.filter(
        status__in=[
            "APPROVED",
            "NOT_APPROVED",
        ]
    )

    return render(
        request,
        "pages/my_trainings.html",
        {
            "pending_assignments": pending_assignments,
            "completed_assignments": completed_assignments,
        },
    )


@login_required
def training_view(request, pk):
    """
    Muestra el visor de una capacitación asignada
    al usuario autenticado.
    """

    assignment = get_object_or_404(
        TrainingAssignment.objects.select_related(
            "training_action",
        ),
        training_action_id=pk,
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    )

    return render(
        request,
        "pages/training_view.html",
        {
            "training": assignment.training_action,
            "assignment": assignment,
        },
    )


@login_required
@xframe_options_sameorigin
def training_content(request, pk):
    """
    Sirve de forma controlada el archivo HTML asociado
    a una capacitación asignada al usuario autenticado.
    """

    assignment = get_object_or_404(
        TrainingAssignment.objects.select_related(
            "training_action",
        ),
        training_action_id=pk,
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    )

    training = assignment.training_action

    if not training.learning_content:
        raise Http404(
            "La capacitación no tiene contenido HTML asociado."
        )

    file_path = Path(training.learning_content.path)

    if not file_path.exists():
        raise Http404(
            "El archivo HTML no existe en el servidor."
        )

    if file_path.suffix.lower() not in {".html", ".htm"}:
        raise Http404(
            "El contenido asociado no es un archivo HTML válido."
        )

    return FileResponse(
        file_path.open("rb"),
        content_type="text/html; charset=utf-8",
    )


@login_required
@require_http_methods(["GET", "POST"])
def training_progress(request, pk):
    """
    Consulta o actualiza el progreso de una capacitación
    para el usuario autenticado.

    GET:
        Devuelve el progreso guardado.

    POST:
        Actualiza etapa actual, módulo actual
        y módulos completados.
    """

    assignment = get_object_or_404(
        TrainingAssignment.objects.select_related(
            "training_action",
            "result",
        ),
        training_action_id=pk,
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    )

    if request.method == "GET":
        training = assignment.training_action

        try:
            result = assignment.result
        except TrainingResult.DoesNotExist:
            result = None

        if result is not None:
            pretest_score = result.pretest_score
            best_posttest_score = result.posttest_score
            improvement_points = result.improvement_points
            attempts_used = result.attempt_number
            approved = result.approved
            completed = result.completed_at is not None
            completed_at = (
                result.completed_at.isoformat()
                if result.completed_at
                else None
            )
        else:
            pretest_score = None
            best_posttest_score = None
            improvement_points = None
            attempts_used = 0
            approved = False
            completed = False
            completed_at = None

        if (
            training.max_attempts is not None
            and training.requires_final_evaluation
        ):
            remaining_attempts = max(
                training.max_attempts - attempts_used,
                0,
            )
        else:
            remaining_attempts = None

        return JsonResponse(
            {
                "ok": True,
                "progress_stage": assignment.progress_stage,
                "current_module": assignment.current_module,
                "completed_modules": assignment.completed_modules,
                "status": assignment.status,
                "requires_pretest": training.requires_pretest,
                "requires_final_evaluation": (
                    training.requires_final_evaluation
                ),
                "passing_score": training.passing_score,
                "max_attempts": training.max_attempts,
                "pretest_score": pretest_score,
                "best_posttest_score": best_posttest_score,
                "improvement_points": improvement_points,
                "attempts_used": attempts_used,
                "remaining_attempts": remaining_attempts,
                "approved": approved,
                "completed": completed,
                "completed_at": completed_at,
            }
        )

    if assignment.status in {
        "APPROVED",
        "NOT_APPROVED",
    }:
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "La capacitación ya fue finalizada "
                    "y su progreso no puede modificarse."
                ),
            },
            status=400,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "Los datos recibidos no tienen un formato válido."
                ),
            },
            status=400,
        )

    progress_stage = data.get(
        "progress_stage",
        assignment.progress_stage,
    )

    current_module = data.get(
        "current_module",
        assignment.current_module,
    )

    completed_modules = data.get(
        "completed_modules",
        assignment.completed_modules,
    )

    valid_stages = {
        "PRETEST",
        "CONTENT",
        "POSTTEST",
        "COMPLETED",
    }

    if progress_stage not in valid_stages:
        return JsonResponse(
            {
                "ok": False,
                "error": "La etapa de progreso no es válida.",
            },
            status=400,
        )

    try:
        current_module = int(current_module)
    except (TypeError, ValueError):
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "El módulo actual debe ser un número entero."
                ),
            },
            status=400,
        )

    if current_module < 0:
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "El módulo actual no puede ser negativo."
                ),
            },
            status=400,
        )

    if not isinstance(completed_modules, list):
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "Los módulos completados deben enviarse "
                    "como una lista."
                ),
            },
            status=400,
        )

    normalized_modules = []

    for module_number in completed_modules:
        try:
            module_number = int(module_number)
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "ok": False,
                    "error": (
                        "Los módulos completados deben contener "
                        "únicamente números enteros."
                    ),
                },
                status=400,
            )

        if module_number < 0:
            return JsonResponse(
                {
                    "ok": False,
                    "error": (
                        "Los números de módulo no pueden ser negativos."
                    ),
                },
                status=400,
            )

        if module_number not in normalized_modules:
            normalized_modules.append(module_number)

    normalized_modules.sort()

    assignment.progress_stage = progress_stage
    assignment.current_module = current_module
    assignment.completed_modules = normalized_modules

    if assignment.status == "PENDING":
        assignment.status = "IN_PROGRESS"

    assignment.full_clean()

    assignment.save(
        update_fields=[
            "progress_stage",
            "current_module",
            "completed_modules",
            "status",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "ok": True,
            "progress_stage": assignment.progress_stage,
            "current_module": assignment.current_module,
            "completed_modules": assignment.completed_modules,
            "status": assignment.status,
        }
    )



@login_required
def certificate_view(request, pk):
    """
    Muestra un certificado activo perteneciente
    al usuario autenticado.
    """

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "assignment",
            "assignment__user",
            "assignment__training_action",
            "assignment__training_action__institution",
        ),
        pk=pk,
        assignment__user=request.user,
        active=True,
    )

    return render(
        request,
        "pages/certificate_detail.html",
        {
            "certificate": certificate,
            "assignment": certificate.assignment,
            "training": certificate.assignment.training_action,
        },
    )



@login_required
def certificate_pdf(request, pk):
    """
    Genera y descarga en PDF un certificado activo
    perteneciente al usuario autenticado.
    """

    certificate = get_object_or_404(
        Certificate.objects.select_related(
            "assignment",
            "assignment__user",
            "assignment__result",
            "assignment__training_action",
            "assignment__training_action__institution",
        ),
        pk=pk,
        assignment__user=request.user,
        active=True,
    )

    assignment = certificate.assignment
    training = assignment.training_action
    result = assignment.result

    buffer = BytesIO()

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height),
        pageCompression=1,
    )

    # --------------------------------------------------
    # PALETA
    # --------------------------------------------------

    teal = colors.HexColor("#0F6B67")
    dark = colors.HexColor("#1F2F33")
    muted = colors.HexColor("#6D7C80")
    gold = colors.HexColor("#D7B46A")
    soft = colors.HexColor("#F8FBFA")

    # --------------------------------------------------
    # FONDO Y MARCOS
    # --------------------------------------------------

    pdf.setFillColor(colors.white)
    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        stroke=0,
        fill=1,
    )

    pdf.setStrokeColor(teal)
    pdf.setLineWidth(4)
    pdf.rect(
        10 * mm,
        10 * mm,
        page_width - 20 * mm,
        page_height - 20 * mm,
        stroke=1,
        fill=0,
    )

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(1)
    pdf.rect(
        15 * mm,
        15 * mm,
        page_width - 30 * mm,
        page_height - 30 * mm,
        stroke=1,
        fill=0,
    )

    # Decoraciones
    pdf.setFillColor(colors.Color(
        teal.red,
        teal.green,
        teal.blue,
        alpha=0.06,
    ))
    pdf.circle(
        page_width - 13 * mm,
        page_height - 13 * mm,
        33 * mm,
        stroke=0,
        fill=1,
    )
    pdf.circle(
        13 * mm,
        13 * mm,
        33 * mm,
        stroke=0,
        fill=1,
    )

    # --------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------

    institution_name = str(training.institution)

    pdf.setFillColor(teal)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 35 * mm,
        institution_name.upper(),
    )

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 53 * mm,
        "CERTIFICADO",
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 62 * mm,
        "ACCIÓN DE FORMACIÓN CONTINUA",
    )

    # --------------------------------------------------
    # PARTICIPANTE
    # --------------------------------------------------

    full_name = (
        assignment.user.get_full_name().strip()
        or assignment.user.username
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 78 * mm,
        "Se certifica que",
    )

    participant_style = ParagraphStyle(
        "Participant",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        textColor=teal,
    )

    participant_paragraph = Paragraph(
        full_name,
        participant_style,
    )

    participant_width = page_width - 70 * mm
    _, participant_height = participant_paragraph.wrap(
        participant_width,
        35 * mm,
    )

    participant_y = page_height - 98 * mm

    participant_paragraph.drawOn(
        pdf,
        (page_width - participant_width) / 2,
        participant_y - participant_height,
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 112 * mm,
        "completó y aprobó satisfactoriamente la capacitación",
    )

    # --------------------------------------------------
    # NOMBRE DE LA CAPACITACION
    # --------------------------------------------------

    training_style = ParagraphStyle(
        "Training",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=dark,
    )

    training_paragraph = Paragraph(
        training.name,
        training_style,
    )

    training_width = page_width - 65 * mm
    _, training_height = training_paragraph.wrap(
        training_width,
        38 * mm,
    )

    training_y = page_height - 126 * mm

    training_paragraph.drawOn(
        pdf,
        (page_width - training_width) / 2,
        training_y - training_height,
    )

    # --------------------------------------------------
    # DATOS PRINCIPALES
    # --------------------------------------------------

    data_y = 42 * mm
    box_width = 50 * mm
    box_height = 20 * mm
    gap = 8 * mm

    total_width = (box_width * 4) + (gap * 3)
    start_x = (page_width - total_width) / 2

    final_date = (
        result.completed_at.strftime("%d/%m/%Y")
        if result.completed_at
        else "-"
    )

    final_score = (
        f"{result.posttest_score} %"
        if result.posttest_score is not None
        else "Aprobado"
    )

    data_items = [
        ("CODIGO", training.code),
        ("VERSION", training.version),
        ("FINALIZACION", final_date),
        ("RESULTADO", final_score),
    ]

    for index, (label, value) in enumerate(data_items):
        x = start_x + index * (box_width + gap)

        pdf.setFillColor(soft)
        pdf.setStrokeColor(colors.HexColor("#D9E2E1"))
        pdf.roundRect(
            x,
            data_y,
            box_width,
            box_height,
            4 * mm,
            stroke=1,
            fill=1,
        )

        pdf.setFillColor(muted)
        pdf.setFont("Helvetica-Bold", 7)
        pdf.drawCentredString(
            x + box_width / 2,
            data_y + 13 * mm,
            label,
        )

        pdf.setFillColor(dark)
        pdf.setFont("Helvetica-Bold", 10)

        value_text = str(value)

        # Acortar visualmente valores muy largos en los cuadros.
        max_width = box_width - 8 * mm

        while (
            stringWidth(
                value_text,
                "Helvetica-Bold",
                10,
            ) > max_width
            and len(value_text) > 3
        ):
            value_text = value_text[:-1]

        if value_text != str(value):
            value_text = value_text[:-2] + "..."

        pdf.drawCentredString(
            x + box_width / 2,
            data_y + 6 * mm,
            value_text,
        )

    # --------------------------------------------------
    # FIRMA Y VERIFICACION
    # --------------------------------------------------

    signature_x = 55 * mm
    signature_y = 19 * mm
    signature_width = 70 * mm

    pdf.setStrokeColor(colors.HexColor("#7B8D8B"))
    pdf.setLineWidth(0.7)
    pdf.line(
        signature_x,
        signature_y + 10 * mm,
        signature_x + signature_width,
        signature_y + 10 * mm,
    )

    pdf.setFillColor(dark)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(
        signature_x + signature_width / 2,
        signature_y + 5 * mm,
        "Responsable institucional",
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 7)
    pdf.drawCentredString(
        signature_x + signature_width / 2,
        signature_y + 1 * mm,
        "Firma autorizada",
    )

    verification_x = page_width - 130 * mm
    verification_y = 14 * mm
    verification_width = 90 * mm
    verification_height = 22 * mm

    pdf.setFillColor(soft)
    pdf.setStrokeColor(colors.HexColor("#D9E2E1"))
    pdf.roundRect(
        verification_x,
        verification_y,
        verification_width,
        verification_height,
        4 * mm,
        stroke=1,
        fill=1,
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica-Bold", 7)
    pdf.drawCentredString(
        verification_x + verification_width / 2,
        verification_y + 15 * mm,
        "CODIGO UNICO DE VERIFICACION",
    )

    verification_code = str(certificate.verification_code)

    pdf.setFillColor(teal)
    pdf.setFont("Courier", 6.5)
    pdf.drawCentredString(
        verification_x + verification_width / 2,
        verification_y + 9 * mm,
        verification_code,
    )

    issued_text = certificate.issued_at.strftime(
        "Emitido el %d/%m/%Y %H:%M"
    )

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 6.5)
    pdf.drawCentredString(
        verification_x + verification_width / 2,
        verification_y + 4 * mm,
        issued_text,
    )

    # --------------------------------------------------
    # NOTA FINAL
    # --------------------------------------------------

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 6.5)
    pdf.drawCentredString(
        page_width / 2,
        11 * mm,
        (
            "Este certificado corresponde a una acción de formación "
            "registrada en HospitalLearning."
        ),
    )

    pdf.showPage()
    pdf.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    safe_training_code = "".join(
        character
        for character in training.code
        if character.isalnum() or character in {"-", "_"}
    )

    filename = (
        f"certificado_{safe_training_code}_"
        f"{certificate.pk}.pdf"
    )

    response = HttpResponse(
        pdf_data,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response

def _parse_score(value, field_name):
    """
    Convierte y valida un puntaje entre 0 y 100.
    """

    try:
        score = int(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"El campo {field_name} debe ser un valor numérico."
        )

    if score < 0 or score > 100:
        raise ValueError(
            f"El campo {field_name} debe estar entre 0 y 100."
        )

    return score


def _result_response(result, training, extra=None):
    """
    Construye la respuesta JSON estándar para el HTML.
    """

    if (
        training.max_attempts is not None
        and training.requires_final_evaluation
    ):
        remaining_attempts = max(
            training.max_attempts - result.attempt_number,
            0,
        )
    else:
        remaining_attempts = None

    data = {
        "ok": True,
        "result_id": result.pk,
        "pretest_score": result.pretest_score,
        "best_posttest_score": result.posttest_score,
        "improvement_points": result.improvement_points,
        "attempts_used": result.attempt_number,
        "max_attempts": training.max_attempts,
        "remaining_attempts": remaining_attempts,
        "approved": result.approved,
        "completed": result.completed_at is not None,
    }

    if extra:
        data.update(extra)

    return JsonResponse(data)


@login_required
@require_POST
def save_training_result(request, pk):
    """
    Recibe eventos enviados por el HTML de la capacitación.

    Eventos admitidos:

    pretest
        Registra una única línea base inicial.

    posttest
        Registra un intento de evaluación final.
        Solo conserva el mejor resultado obtenido.

    finish
        Finaliza formalmente la capacitación.
    """

    assignment = get_object_or_404(
        TrainingAssignment.objects.select_related(
            "training_action",
        ),
        training_action_id=pk,
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    )

    training = assignment.training_action

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "Los datos recibidos no tienen un formato válido."
                ),
            },
            status=400,
        )

    action = data.get("action")

    if action not in {
        "pretest",
        "posttest",
        "finish",
    }:
        return JsonResponse(
            {
                "ok": False,
                "error": "La acción recibida no es válida.",
            },
            status=400,
        )

    result, _ = TrainingResult.objects.get_or_create(
        assignment=assignment,
    )

    if action == "pretest":

        if result.completed_at is not None:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "La capacitación ya fue finalizada.",
                },
                status=400,
            )

        if not training.requires_pretest:
            return _result_response(
                result,
                training,
                {
                    "pretest_required": False,
                    "message": (
                        "La capacitación no requiere pretest."
                    ),
                },
            )

        try:
            pretest_score = _parse_score(
                data.get("pretest_score"),
                "pretest_score",
            )
        except ValueError as error:
            return JsonResponse(
                {
                    "ok": False,
                    "error": str(error),
                },
                status=400,
            )

        if result.pretest_score is None:
            result.pretest_score = pretest_score
            result.full_clean()
            result.save()

        assignment.progress_stage = "CONTENT"

        if assignment.status == "PENDING":
            assignment.status = "IN_PROGRESS"

        assignment.save(
            update_fields=[
                "progress_stage",
                "status",
                "updated_at",
            ]
        )

        return _result_response(
            result,
            training,
            {
                "message": "Pretest registrado correctamente.",
            },
        )

    if action == "posttest":

        if result.completed_at is not None:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "La capacitación ya fue finalizada.",
                },
                status=400,
            )

        if not training.requires_final_evaluation:
            return _result_response(
                result,
                training,
                {
                    "posttest_required": False,
                    "message": (
                        "La capacitación no requiere evaluación final."
                    ),
                },
            )

        if (
            training.requires_pretest
            and result.pretest_score is None
        ):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Debe registrarse primero el pretest.",
                },
                status=400,
            )

        if (
            training.max_attempts is not None
            and result.attempt_number >= training.max_attempts
        ):
            return JsonResponse(
                {
                    "ok": False,
                    "error": (
                        "Ya se alcanzó el número máximo "
                        "de intentos de postest."
                    ),
                },
                status=400,
            )

        try:
            posttest_score = _parse_score(
                data.get("posttest_score"),
                "posttest_score",
            )
        except ValueError as error:
            return JsonResponse(
                {
                    "ok": False,
                    "error": str(error),
                },
                status=400,
            )

        result.attempt_number += 1

        if (
            result.posttest_score is None
            or posttest_score > result.posttest_score
        ):
            result.posttest_score = posttest_score

        result.full_clean()
        result.save()

        assignment.progress_stage = "POSTTEST"

        if assignment.status == "PENDING":
            assignment.status = "IN_PROGRESS"

        assignment.save(
            update_fields=[
                "progress_stage",
                "status",
                "updated_at",
            ]
        )

        if training.max_attempts is None:
            can_retry = True
        else:
            can_retry = (
                result.attempt_number < training.max_attempts
            )

        return _result_response(
            result,
            training,
            {
                "current_posttest_score": posttest_score,
                "can_retry": can_retry,
                "message": (
                    "Intento de postest registrado correctamente."
                ),
            },
        )

    if action == "finish":

        if result.completed_at is not None:
            return _result_response(
                result,
                training,
                {
                    "message": (
                        "La capacitación ya había sido finalizada."
                    ),
                },
            )

        if (
            training.requires_pretest
            and result.pretest_score is None
        ):
            return JsonResponse(
                {
                    "ok": False,
                    "error": (
                        "No puede finalizar porque falta el pretest."
                    ),
                },
                status=400,
            )

        if (
            training.requires_final_evaluation
            and result.posttest_score is None
        ):
            return JsonResponse(
                {
                    "ok": False,
                    "error": (
                        "No puede finalizar porque falta el postest."
                    ),
                },
                status=400,
            )

        if training.requires_final_evaluation:
            passing_score = training.passing_score or 0

            result.approved = (
                result.posttest_score >= passing_score
            )
        else:
            result.approved = True

        result.completed_at = timezone.now()

        result.full_clean()
        result.save()

        assignment.progress_stage = "COMPLETED"

        if result.approved:
            assignment.status = "APPROVED"
        else:
            assignment.status = "NOT_APPROVED"

        assignment.save(
            update_fields=[
                "progress_stage",
                "status",
                "updated_at",
            ]
        )

        certificate = None
        certificate_created = False

        if (
            result.approved
            and training.generates_certificate
            and training.automatic_certificate
        ):
            certificate, certificate_created = (
                Certificate.objects.get_or_create(
                    assignment=assignment,
                )
            )

        extra_data = {
            "message": (
                "Capacitación finalizada correctamente."
            ),
            "certificate_available": certificate is not None,
            "certificate_created": certificate_created,
        }

        if certificate is not None:
            extra_data["certificate_id"] = certificate.pk
            extra_data["verification_code"] = str(
                certificate.verification_code
            )

        return _result_response(
            result,
            training,
            extra_data,
        )