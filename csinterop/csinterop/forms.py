from django import forms
from csinterop.models import InteropService


class InteropServiceForm(forms.ModelForm):
    services = forms.ModelChoiceField(queryset=InteropService.objects.all().order_by('name'))

    class Meta:
        model = InteropService
        fields = ['services']
        widgets = {
            'services': forms.Select(attrs={'class': 'form-control'}, )
        }