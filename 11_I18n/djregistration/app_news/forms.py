from django import forms
from django.utils.translation import gettext_lazy as _

from djregistration import settings


class NewsItemForm(forms.Form):
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
    tag = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('tid_news_form_placeholder_tag'),
            }
        )
    )


class SearchTag(forms.Form):
    tag = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('tid_tag_search_form_placeholder_tag'),
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
                'placeholder': _('tid_tag_search_form_placeholder_date')
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
