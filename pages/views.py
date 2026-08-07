from pathlib import Path

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from training.models import TrainingAction, TrainingAssignment


def home(request):
    return render(request, "pages/home.html")


def my_trainings(request):
    """
    Muestra las capacitaciones asignadas al usuario autenticado.
    """

    assignments = TrainingAssignment.objects.filter(
        user=request.user,
        training_action__active=True,
        training_action__status="PUBLISHED",
    ).select_related(
        "training_action",
        "training_action__action_type",
        "training_action__institution",
    )

    return render(
        request,
        "pages/my_trainings.html",
        {
            "assignments": assignments,
        },
    )


def training_view(request, pk):
    """
    Muestra la pantalla que contiene el visor de la capacitación.
    """

    training = get_object_or_404(
        TrainingAction,
        pk=pk,
        active=True,
        status="PUBLISHED",
    )

    return render(
        request,
        "pages/training_view.html",
        {
            "training": training,
        },
    )


@xframe_options_sameorigin
def training_content(request, pk):
    """
    Sirve de forma controlada el archivo HTML asociado a la capacitación.
    """

    training = get_object_or_404(
        TrainingAction,
        pk=pk,
        active=True,
        status="PUBLISHED",
    )

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