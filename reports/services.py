from datetime import date

from certificates.models import Certificate
from training.models import ActionType, TrainingAction, TrainingAssignment, TrainingResult
from users.models import CustomUser, InstitutionalLink


FINAL_STATUSES = {"APPROVED", "NOT_APPROVED"}
OPEN_STATUSES = {"PENDING", "IN_PROGRESS", "EXPIRED"}


def get_report_context(institution, params):
    base_assignments = (
        TrainingAssignment.objects.filter(
            training_action__institution=institution,
        )
        .select_related(
            "user",
            "training_action",
            "training_action__action_type",
            "training_action__institution",
        )
        .order_by("-assigned_at", "training_action__name", "user__username")
    )

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
        TrainingAssignment._meta.get_field("status").choices
    )

    selected = {
        "training_action": (params.get("training_action") or "").strip(),
        "action_type": (params.get("action_type") or "").strip(),
        "profession": (params.get("profession") or "").strip(),
        "status": (params.get("status") or "").strip(),
        "date_from": (params.get("date_from") or "").strip(),
        "date_to": (params.get("date_to") or "").strip(),
        "participant": (params.get("participant") or "").strip(),
        "mandatory": (params.get("mandatory") or "").strip(),
        "generates_certificate": (
            params.get("generates_certificate") or ""
        ).strip(),
    }

    assignments = base_assignments

    selected_action = None
    selected_action_type = None
    selected_participant = None

    if selected["date_from"]:
        try:
            parsed = date.fromisoformat(selected["date_from"])
        except ValueError:
            selected["date_from"] = ""
        else:
            assignments = assignments.filter(assigned_at__date__gte=parsed)

    if selected["date_to"]:
        try:
            parsed = date.fromisoformat(selected["date_to"])
        except ValueError:
            selected["date_to"] = ""
        else:
            assignments = assignments.filter(assigned_at__date__lte=parsed)

    if selected["participant"]:
        try:
            selected_participant = available_participants.get(
                pk=selected["participant"]
            )
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            selected["participant"] = ""
            selected_participant = None
        else:
            assignments = assignments.filter(user=selected_participant)

    if selected["profession"]:
        if selected["profession"] not in available_professions:
            selected["profession"] = ""
        else:
            assignments = assignments.filter(
                user__profession=selected["profession"]
            )

    valid_statuses = {value for value, _label in available_statuses}
    if selected["status"]:
        if selected["status"] not in valid_statuses:
            selected["status"] = ""
        else:
            assignments = assignments.filter(status=selected["status"])

    if selected["mandatory"] in {"yes", "no"}:
        assignments = assignments.filter(
            training_action__mandatory=(selected["mandatory"] == "yes")
        )
    else:
        selected["mandatory"] = ""

    if selected["generates_certificate"] in {"yes", "no"}:
        assignments = assignments.filter(
            training_action__generates_certificate=(
                selected["generates_certificate"] == "yes"
            )
        )
    else:
        selected["generates_certificate"] = ""

    if selected["action_type"]:
        try:
            selected_action_type = available_action_types.get(
                pk=selected["action_type"]
            )
        except (ActionType.DoesNotExist, ValueError, TypeError):
            selected["action_type"] = ""
            selected_action_type = None
        else:
            assignments = assignments.filter(
                training_action__action_type=selected_action_type
            )

    if selected["training_action"]:
        try:
            selected_action = available_training_actions.get(
                pk=selected["training_action"]
            )
        except (TrainingAction.DoesNotExist, ValueError, TypeError):
            selected["training_action"] = ""
            selected_action = None
        else:
            assignments = assignments.filter(
                training_action=selected_action
            )

    assignments = list(assignments)

    assignment_ids = [assignment.id for assignment in assignments]

    results_by_assignment = {
        result.assignment_id: result
        for result in TrainingResult.objects.filter(
            assignment_id__in=assignment_ids
        )
    }

    certificates_by_assignment = {
        certificate.assignment_id: certificate
        for certificate in Certificate.objects.filter(
            assignment_id__in=assignment_ids,
            active=True,
        )
    }

    detail_rows = []
    action_map = {}
    participant_map = {}
    profession_map = {}
    evaluation_rows = []
    certificate_rows = []
    pending_rows = []

    for assignment in assignments:
        user = assignment.user
        training = assignment.training_action
        result = results_by_assignment.get(assignment.id)
        certificate = certificates_by_assignment.get(assignment.id)

        full_name = user.get_full_name().strip() or user.username
        document = "—"
        if user.document_number:
            document = (
                f"{user.document_type} {user.document_number}".strip()
            )

        completed = assignment.status in FINAL_STATUSES

        row = {
            "assignment_id": assignment.id,
            "participant": full_name,
            "username": user.username,
            "document": document,
            "profession": user.profession or "—",
            "training": training.name,
            "code": training.code,
            "action_type": (
                training.action_type.name
                if training.action_type is not None
                else "—"
            ),
            "mandatory": "Sí" if training.mandatory else "No",
            "assigned_at": assignment.assigned_at,
            "due_date": assignment.due_date,
            "status": assignment.get_status_display(),
            "status_code": assignment.status,
            "pretest": result.pretest_score if result else None,
            "posttest": result.posttest_score if result else None,
            "improvement": result.improvement_points if result else None,
            "attempts": result.attempt_number if result else 0,
            "completed_at": result.completed_at if result else None,
            "approved": (
                result.approved
                if result is not None
                else assignment.status == "APPROVED"
            ),
            "generates_certificate": (
                "Sí" if training.generates_certificate else "No"
            ),
            "certificate": certificate,
            "certificate_issued_at": (
                certificate.issued_at if certificate else None
            ),
            "completed": completed,
        }
        detail_rows.append(row)

        action_key = training.id
        if action_key not in action_map:
            action_map[action_key] = {
                "training": training.name,
                "code": training.code,
                "action_type": row["action_type"],
                "assigned": 0,
                "pending": 0,
                "in_progress": 0,
                "approved": 0,
                "not_approved": 0,
                "expired": 0,
                "completed": 0,
                "posttests": [],
                "certificates": 0,
            }

        action_summary = action_map[action_key]
        action_summary["assigned"] += 1
        if assignment.status == "PENDING":
            action_summary["pending"] += 1
        elif assignment.status == "IN_PROGRESS":
            action_summary["in_progress"] += 1
        elif assignment.status == "APPROVED":
            action_summary["approved"] += 1
            action_summary["completed"] += 1
        elif assignment.status == "NOT_APPROVED":
            action_summary["not_approved"] += 1
            action_summary["completed"] += 1
        elif assignment.status == "EXPIRED":
            action_summary["expired"] += 1

        if result and result.posttest_score is not None:
            action_summary["posttests"].append(result.posttest_score)
        if certificate:
            action_summary["certificates"] += 1

        participant_key = user.id
        if participant_key not in participant_map:
            participant_map[participant_key] = {
                "participant": full_name,
                "username": user.username,
                "document": document,
                "profession": user.profession or "—",
                "assigned": 0,
                "completed": 0,
                "approved": 0,
                "not_approved": 0,
                "pending": 0,
                "in_progress": 0,
                "expired": 0,
                "posttests": [],
                "certificates": 0,
            }

        participant_summary = participant_map[participant_key]
        participant_summary["assigned"] += 1
        if assignment.status == "PENDING":
            participant_summary["pending"] += 1
        elif assignment.status == "IN_PROGRESS":
            participant_summary["in_progress"] += 1
        elif assignment.status == "APPROVED":
            participant_summary["approved"] += 1
            participant_summary["completed"] += 1
        elif assignment.status == "NOT_APPROVED":
            participant_summary["not_approved"] += 1
            participant_summary["completed"] += 1
        elif assignment.status == "EXPIRED":
            participant_summary["expired"] += 1

        if result and result.posttest_score is not None:
            participant_summary["posttests"].append(result.posttest_score)
        if certificate:
            participant_summary["certificates"] += 1

        profession_key = user.profession or "Sin profesión registrada"
        if profession_key not in profession_map:
            profession_map[profession_key] = {
                "profession": profession_key,
                "assigned": 0,
                "completed": 0,
                "approved": 0,
                "not_approved": 0,
                "pending": 0,
                "in_progress": 0,
                "expired": 0,
            }

        profession_summary = profession_map[profession_key]
        profession_summary["assigned"] += 1
        if assignment.status == "PENDING":
            profession_summary["pending"] += 1
        elif assignment.status == "IN_PROGRESS":
            profession_summary["in_progress"] += 1
        elif assignment.status == "APPROVED":
            profession_summary["approved"] += 1
            profession_summary["completed"] += 1
        elif assignment.status == "NOT_APPROVED":
            profession_summary["not_approved"] += 1
            profession_summary["completed"] += 1
        elif assignment.status == "EXPIRED":
            profession_summary["expired"] += 1

        if result is not None:
            evaluation_rows.append(row)

        if certificate is not None:
            certificate_rows.append(row)

        if assignment.status in OPEN_STATUSES:
            pending_rows.append(row)

    action_summary_rows = []
    for item in action_map.values():
        item["compliance"] = (
            round(item["completed"] / item["assigned"] * 100, 1)
            if item["assigned"]
            else 0
        )
        item["posttest_average"] = (
            round(sum(item["posttests"]) / len(item["posttests"]), 1)
            if item["posttests"]
            else None
        )
        action_summary_rows.append(item)

    action_summary_rows.sort(key=lambda item: item["training"].lower())

    participant_summary_rows = []
    for item in participant_map.values():
        item["compliance"] = (
            round(item["completed"] / item["assigned"] * 100, 1)
            if item["assigned"]
            else 0
        )
        item["posttest_average"] = (
            round(sum(item["posttests"]) / len(item["posttests"]), 1)
            if item["posttests"]
            else None
        )
        participant_summary_rows.append(item)

    participant_summary_rows.sort(
        key=lambda item: item["participant"].lower()
    )

    profession_summary_rows = []
    for item in profession_map.values():
        item["compliance"] = (
            round(item["completed"] / item["assigned"] * 100, 1)
            if item["assigned"]
            else 0
        )
        profession_summary_rows.append(item)

    profession_summary_rows.sort(
        key=lambda item: item["profession"].lower()
    )

    total_assignments = len(detail_rows)
    total_completed = sum(1 for row in detail_rows if row["completed"])
    total_approved = sum(
        1 for row in detail_rows if row["status_code"] == "APPROVED"
    )
    total_certificates = len(certificate_rows)

    summary = {
        "assignments": total_assignments,
        "participants": len(participant_map),
        "completed": total_completed,
        "approved": total_approved,
        "pending": len(pending_rows),
        "certificates": total_certificates,
        "compliance": (
            round(total_completed / total_assignments * 100, 1)
            if total_assignments
            else 0
        ),
    }

    return {
        "summary": summary,
        "detail_rows": detail_rows,
        "action_summary_rows": action_summary_rows,
        "participant_summary_rows": participant_summary_rows,
        "profession_summary_rows": profession_summary_rows,
        "evaluation_rows": evaluation_rows,
        "certificate_rows": certificate_rows,
        "pending_rows": pending_rows,
        "available_training_actions": available_training_actions,
        "available_action_types": available_action_types,
        "available_professions": available_professions,
        "available_participants": available_participants,
        "available_statuses": available_statuses,
        "selected": selected,
        "selected_action": selected_action,
        "selected_action_type": selected_action_type,
        "selected_participant": selected_participant,
    }