from django.contrib.gis import forms
from .models import Home, Module


class HomeForm(forms.Form):
    name = forms.CharField(
        min_length=1,
        max_length=255,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    lat = forms.FloatField(
        widget=forms.HiddenInput()
    )
    lng = forms.FloatField(
        widget=forms.HiddenInput()
    )
    radius = forms.IntegerField(
        max_value='1000000000',
        min_value='5',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=50
    )
    module = forms.ModelChoiceField(
        widget=forms.RadioSelect,
        queryset=Module.objects.all(),
        empty_label='モジュールを選択',
        required=True
    )

    class Meta:
        labels = {
            'radius': 'Radius',
            'name': 'Name',
            'module': 'Module'
        }
