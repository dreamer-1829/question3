from django import forms
from .models import WeightEntry

class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight']

class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
