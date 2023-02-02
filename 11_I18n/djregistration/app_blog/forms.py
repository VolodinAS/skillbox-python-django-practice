from django import forms
from django.utils.translation import gettext_lazy as _


class BlogAddForm(forms.Form):
    header = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('tid_blog_form_placeholder_header')
            }
        )
    )
    content = forms.CharField(
        max_length=5000,
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('tid_blog_form_placeholder_content'),
                'rows': 5
            }
        )
    )
    images = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
            }
        )
    )


class BlogImportForm(forms.Form):
    csv_files = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'multiple': True,
                'class': 'custom-file-input',
                'accept': '.csv'
            }
        )
    )
