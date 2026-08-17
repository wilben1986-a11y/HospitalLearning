from django import forms

from training.models import TrainingAction

from .models import DocumentResource, MediaResource


class DocumentResourceForm(forms.ModelForm):
    class Meta:
        model = DocumentResource
        fields = (
            "title",
            "document_type",
            "description",
            "file",
            "version",
            "document_date",
            "training_actions",
            "active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "document_date": forms.DateInput(attrs={"type": "date"}),
            "training_actions": forms.SelectMultiple(
                attrs={"class": "form-select", "size": 8}
            ),
        }

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.institution = institution

        for field in self.fields.values():
            current_class = field.widget.attrs.get("class", "")
            if "form-control" not in current_class and "form-select" not in current_class:
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs["class"] = "form-check-input"
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs["class"] = "form-select"
                else:
                    field.widget.attrs["class"] = "form-control"

        if institution is not None:
            self.fields["training_actions"].queryset = (
                TrainingAction.objects.filter(
                    institution=institution,
                    active=True,
                )
                .order_by("name")
            )
        else:
            self.fields["training_actions"].queryset = (
                TrainingAction.objects.none()
            )

    def clean_training_actions(self):
        actions = self.cleaned_data["training_actions"]

        if self.institution is not None:
            invalid = actions.exclude(institution=self.institution)

            if invalid.exists():
                raise forms.ValidationError(
                    "Solo puede asociar capacitaciones de la institución activa."
                )

        return actions


class MediaResourceForm(forms.ModelForm):
    class Meta:
        model = MediaResource
        fields = (
            "title",
            "media_type",
            "description",
            "file",
            "external_url",
            "training_actions",
            "active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "training_actions": forms.SelectMultiple(
                attrs={"class": "form-select", "size": 8}
            ),
        }

    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.institution = institution

        for field in self.fields.values():
            current_class = field.widget.attrs.get("class", "")
            if "form-control" not in current_class and "form-select" not in current_class:
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs["class"] = "form-check-input"
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs["class"] = "form-select"
                else:
                    field.widget.attrs["class"] = "form-control"

        if institution is not None:
            self.fields["training_actions"].queryset = (
                TrainingAction.objects.filter(
                    institution=institution,
                    active=True,
                )
                .order_by("name")
            )
        else:
            self.fields["training_actions"].queryset = (
                TrainingAction.objects.none()
            )

    def clean(self):
        cleaned_data = super().clean()

        file = cleaned_data.get("file")
        external_url = cleaned_data.get("external_url")

        if not file and not external_url:
            raise forms.ValidationError(
                "Debe proporcionar un archivo o un enlace externo."
            )

        return cleaned_data

    def clean_training_actions(self):
        actions = self.cleaned_data["training_actions"]

        if self.institution is not None:
            invalid = actions.exclude(institution=self.institution)

            if invalid.exists():
                raise forms.ValidationError(
                    "Solo puede asociar capacitaciones de la institución activa."
                )

        return actions