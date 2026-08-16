import csv
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .services import get_active_institution, get_report_context


def _require_institutional_access(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied(
            "No tienes permisos para consultar reportes institucionales."
        )

    institution, institutional_link = get_active_institution(request.user)

    if institution is None:
        raise PermissionDenied(
            "Tu usuario no tiene una institución activa asociada."
        )

    return institution, institutional_link


@login_required
def institutional_reports(request):
    institution, institutional_link = _require_institutional_access(request)

    report_data = get_report_context(
        institution,
        request.GET,
    )

    context = {
        "institution": institution,
        "institutional_link": institutional_link,
        **report_data,
    }

    return render(
        request,
        "reports/institutional_reports.html",
        context,
    )


@login_required
def export_csv(request, report_type):
    institution, _institutional_link = _require_institutional_access(request)

    data = get_report_context(
        institution,
        request.GET,
    )

    report_map = {
        "cumplimiento": (
            data["detail_rows"],
            [
                ("Participante", "participant"),
                ("Documento", "document"),
                ("Profesión", "profession"),
                ("Capacitación", "training"),
                ("Código", "code"),
                ("Tipo", "action_type"),
                ("Obligatoria", "mandatory"),
                ("Fecha asignación", "assigned_at"),
                ("Fecha límite", "due_date"),
                ("Estado", "status"),
                ("Pretest", "pretest"),
                ("Postest", "posttest"),
                ("Mejora", "improvement"),
                ("Intentos", "attempts"),
                ("Fecha finalización", "completed_at"),
                ("Genera certificado", "generates_certificate"),
                ("Certificado emitido", "certificate_issued_at"),
            ],
        ),
        "pendientes": (
            data["pending_rows"],
            [
                ("Participante", "participant"),
                ("Documento", "document"),
                ("Profesión", "profession"),
                ("Capacitación", "training"),
                ("Código", "code"),
                ("Fecha asignación", "assigned_at"),
                ("Fecha límite", "due_date"),
                ("Estado", "status"),
            ],
        ),
        "evaluaciones": (
            data["evaluation_rows"],
            [
                ("Participante", "participant"),
                ("Capacitación", "training"),
                ("Pretest", "pretest"),
                ("Postest", "posttest"),
                ("Mejora", "improvement"),
                ("Intentos", "attempts"),
                ("Estado", "status"),
                ("Fecha finalización", "completed_at"),
            ],
        ),
        "certificados": (
            data["certificate_rows"],
            [
                ("Participante", "participant"),
                ("Documento", "document"),
                ("Capacitación", "training"),
                ("Código", "code"),
                ("Estado", "status"),
                ("Fecha finalización", "completed_at"),
                ("Fecha emisión", "certificate_issued_at"),
            ],
        ),
        "acciones": (
            data["action_summary_rows"],
            [
                ("Capacitación", "training"),
                ("Código", "code"),
                ("Tipo", "action_type"),
                ("Asignadas", "assigned"),
                ("Completadas", "completed"),
                ("Aprobadas", "approved"),
                ("No aprobadas", "not_approved"),
                ("Pendientes", "pending"),
                ("En progreso", "in_progress"),
                ("Vencidas", "expired"),
                ("Cumplimiento", "compliance"),
                ("Promedio postest", "posttest_average"),
                ("Certificados", "certificates"),
            ],
        ),
        "participantes": (
            data["participant_summary_rows"],
            [
                ("Participante", "participant"),
                ("Usuario", "username"),
                ("Documento", "document"),
                ("Profesión", "profession"),
                ("Asignadas", "assigned"),
                ("Completadas", "completed"),
                ("Aprobadas", "approved"),
                ("No aprobadas", "not_approved"),
                ("Pendientes", "pending"),
                ("En progreso", "in_progress"),
                ("Vencidas", "expired"),
                ("Cumplimiento", "compliance"),
                ("Promedio postest", "posttest_average"),
                ("Certificados", "certificates"),
            ],
        ),
        "profesiones": (
            data["profession_summary_rows"],
            [
                ("Profesión", "profession"),
                ("Asignadas", "assigned"),
                ("Completadas", "completed"),
                ("Aprobadas", "approved"),
                ("No aprobadas", "not_approved"),
                ("Pendientes", "pending"),
                ("En progreso", "in_progress"),
                ("Vencidas", "expired"),
                ("Cumplimiento", "compliance"),
            ],
        ),
    }

    if report_type not in report_map:
        raise PermissionDenied("Tipo de reporte no válido.")

    rows, columns = report_map[report_type]

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="reporte_{report_type}.csv"'
    )
    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";")
    writer.writerow([label for label, _key in columns])

    for row in rows:
        values = []
        for _label, key in columns:
            value = row.get(key)
            if hasattr(value, "strftime"):
                value = value.strftime("%d/%m/%Y %H:%M")
            if value is None:
                value = ""
            values.append(value)
        writer.writerow(values)

    return response


@login_required
def export_pdf(request):
    institution, _institutional_link = _require_institutional_access(request)

    data = get_report_context(
        institution,
        request.GET,
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph(
            f"Reporte institucional - {institution}",
            styles["Title"],
        )
    )
    story.append(Spacer(1, 6 * mm))

    summary = data["summary"]
    summary_table = Table(
        [
            [
                "Asignaciones",
                "Participantes",
                "Completadas",
                "Aprobadas",
                "Pendientes",
                "Certificados",
                "Cumplimiento",
            ],
            [
                summary["assignments"],
                summary["participants"],
                summary["completed"],
                summary["approved"],
                summary["pending"],
                summary["certificates"],
                f'{summary["compliance"]} %',
            ],
        ],
        repeatRows=1,
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9ECEF")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 7 * mm))

    story.append(Paragraph("Detalle de cumplimiento", styles["Heading2"]))
    story.append(Spacer(1, 3 * mm))

    table_data = [
        [
            "Participante",
            "Profesión",
            "Capacitación",
            "Asignación",
            "Estado",
            "Pretest",
            "Postest",
            "Certificado",
        ]
    ]

    for row in data["detail_rows"]:
        table_data.append(
            [
                row["participant"],
                row["profession"],
                row["training"],
                (
                    row["assigned_at"].strftime("%d/%m/%Y")
                    if row["assigned_at"]
                    else ""
                ),
                row["status"],
                row["pretest"] if row["pretest"] is not None else "",
                row["posttest"] if row["posttest"] is not None else "",
                "Sí" if row["certificate"] else "No",
            ]
        )

    detail_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            38 * mm,
            28 * mm,
            58 * mm,
            22 * mm,
            24 * mm,
            18 * mm,
            18 * mm,
            20 * mm,
        ],
    )

    detail_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9ECEF")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 6.8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    story.append(detail_table)

    document.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )
    response["Content-Disposition"] = (
        'attachment; filename="reporte_institucional.pdf"'
    )
    return response