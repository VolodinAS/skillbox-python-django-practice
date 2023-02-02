from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment


class CommentForm(forms.ModelForm):
    
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _("tid_comment_form_text")
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ['text']
