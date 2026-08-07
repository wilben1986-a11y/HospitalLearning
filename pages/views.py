import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from training.models import (
    TrainingAction,
    TrainingAssignment,
    TrainingResult,
)


def home(request):
    return render(request, "pages/home.html")


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

        if assignment.status == "PENDING":
            assignment.status = "IN_PROGRESS"
            assignment.save(
                update_fields=[
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

        if assignment.status == "PENDING":
            assignment.status = "IN_PROGRESS"
            assignment.save(
                update_fields=[
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

        if result.approved:
            assignment.status = "APPROVED"
        else:
            assignment.status = "NOT_APPROVED"

        assignment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return _result_response(
            result,
            training,
            {
                "message": (
                    "Capacitación finalizada correctamente."
                ),
            },
        )