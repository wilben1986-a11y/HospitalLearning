from django import forms
from training.models import ActionType
from .models import Institution, Service

def _bootstrap(form):
    for field in form.fields.values():
        w = field.widget
        if isinstance(w, forms.CheckboxInput):
            w.attrs["class"] = "form-check-input"
        elif isinstance(w, forms.Select):
            w.attrs["class"] = "form-select"
        else:
            w.attrs["class"] = (w.attrs.get("class", "") + " form-control").strip()

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ("name", "nit", "code")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); _bootstrap(self)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "parent", "active")
    def __init__(self, *args, institution=None, **kwargs):
        super().__init__(*args, **kwargs); self.institution = institution
        qs = Service.objects.filter(institution=institution).order_by("name") if institution else Service.objects.none()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        self.fields["parent"].queryset = qs
        _bootstrap(self)
    def clean_parent(self):
        parent = self.cleaned_data.get("parent")
        if parent and self.institution and parent.institution_id != self.institution.id:
            raise forms.ValidationError("El servicio principal debe pertenecer a la institución activa.")
        return parent

class ActionTypeForm(forms.ModelForm):
    class Meta:
        model = ActionType
        fields = ("name","code","objective","description","active","requires_certificate","has_validity","requires_renewal","renewal_period_months","new_version_requires_retake")
        widgets = {"objective": forms.Textarea(attrs={"rows":3}), "description": forms.Textarea(attrs={"rows":3})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); _bootstrap(self)