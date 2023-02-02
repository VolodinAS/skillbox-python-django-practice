from django import forms

from djregistration import settings


class NewsItemForm(forms.Form):
    header = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': 'Заголовок, 200 символов'
            }
        )
    )
    content = forms.CharField(
        max_length=5000,
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': 'Описание новости, 5000 символов',
                'rows': 5
            }
        )
    )
    tag = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': 'Тег новости, 20 символов',
            }
        )
    )
    
    # class Meta:
    #     model = NewsItem
    #     fields = ['header', 'content', '']


class SearchTag(forms.Form):
    tag = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Искомый тег новости, 20 символов',
                'autofocus': True
            }
        )
    )
    dater = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control',
                'placeholder': 'От даты'
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
