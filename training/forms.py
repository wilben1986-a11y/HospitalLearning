from django import forms

from users.models import CustomUser, InstitutionalLink

from .models import ActionType, TrainingAction


def _apply_bootstrap(form):
    for field in form.fields.values():
        widget = field.widget

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs["class"] = "form-check-input"
        elif isinstance(widget, forms.Select):
            widget.attrs["class"] = "form-select"
        elif isinstance(widget, forms.ClearableFileInput):
            widget.attrs["class"] = "form-control"
        else:
            current = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{current} form-control".strip()


class TrainingActionForm(forms.ModelForm):
    class Meta:
        model = TrainingAction
        fields = (
            "action_type",
            "name",
            "code",
            "objective",
            "description",
            "learning_content",
            "version",
            "status",
            "publication_date",
            "active",
            "mandatory",
            "requires_pretest",
            "requires_final_evaluation",
            "requires_complete_content",
            "passing_score",
            "max_attempts",
            "generates_certificate",
            "automatic_certificate",
        )
        widgets = {
            "objective": forms.Textarea(attrs={"rows": 4}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "publication_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institution = institution

        if institution is not None:
            self.fields["action_type"].queryset = (
                ActionType.objects.filter(
                    institution=institution,
                    active=True,
                )
                .order_by("name")
            )
        else:
            self.fields["action_type"].queryset = ActionType.objects.none()

        _apply_bootstrap(self)

    def clean_action_type(self):
        action_type = self.cleaned_data.get("action_type")

        if (
            action_type is not None
            and self.institution is not None
            and action_type.institution_id != self.institution.id
        ):
            raise forms.ValidationError(
                "El tipo de acción debe pertenecer a la institución activa."
            )

        return action_type

    def clean(self):
        cleaned_data = super().clean()

        requires_final = cleaned_data.get("requires_final_evaluation")
        passing_score = cleaned_data.get("passing_score")
        max_attempts = cleaned_data.get("max_attempts")
        generates_certificate = cleaned_data.get("generates_certificate")
        automatic_certificate = cleaned_data.get("automatic_certificate")

        if requires_final and passing_score is None:
            self.add_error(
                "passing_score",
                "Debe indicar el puntaje mínimo de aprobación.",
            )

        if passing_score is not None and passing_score > 100:
            self.add_error(
                "passing_score",
                "El puntaje mínimo no puede superar 100.",
            )

        if max_attempts is not None and max_attempts < 1:
            self.add_error(
                "max_attempts",
                "El número máximo de intentos debe ser mayor que cero.",
            )

        if not requires_final:
            cleaned_data["passing_score"] = None
            cleaned_data["max_attempts"] = None

        if automatic_certificate and not generates_certificate:
            self.add_error(
                "automatic_certificate",
                "Para emitir certificados automáticamente debe activar "
                "'Genera certificado'.",
            )

        return cleaned_data


class BulkTrainingAssignmentForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        label="Participantes",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
                "size": 12,
            }
        ),
        help_text=(
            "Seleccione uno o varios participantes vinculados activamente "
            "a la institución."
        ),
    )

    due_date = forms.DateField(
        required=False,
        label="Fecha límite",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    observations = forms.CharField(
        required=False,
        label="Observaciones",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
            }
        ),
    )

    def __init__(self, *args, institution=None, training_action=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institution = institution
        self.training_action = training_action

        if institution is None:
            return

        linked_user_ids = (
            InstitutionalLink.objects.filter(
                institution=institution,
                active=True,
                user__is_active=True,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )

        queryset = (
            CustomUser.objects.filter(id__in=linked_user_ids)
            .order_by("last_name", "first_name", "username")
        )

        if training_action is not None:
            queryset = queryset.exclude(
                training_assignments__training_action=training_action
            )

        self.fields["participants"].queryset = queryset