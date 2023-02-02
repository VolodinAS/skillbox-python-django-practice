from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Текст комментария'
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ['text']
