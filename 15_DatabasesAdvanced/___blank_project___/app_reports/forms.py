from django import forms
from django.conf import settings


class ReportForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control',
                'placeholder': 'Начало периода'
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    date_to = forms.DateTimeField(
        required=False,
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control',
                'placeholder': 'Конец периода'
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
