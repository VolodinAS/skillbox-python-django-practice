from django import forms

from .models import NewsItem, Comment

form_control_lg_mtb_3 = 'form-control mb-3'


class EditNewsForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = [
            'header',
            'content',
            'activity'
        ]
        # widgets = {
        #     'header': forms.TextInput(
        #         attrs={
        #             'class': form_control_lg_mtb_3,
        #             'placeholder': 'Заголовок новости'
        #         }
        #     ),
        #     # 'content': forms.CharField(
        #     #     widget=forms.Textarea(
        #     #         attrs={
        #     #             'class': form_control_lg_mtb_3,
        #     #             'rows': 5,
        #     #             'placeholder': 'Текст новости'
        #     #         }
        #     #     )
        #     # ),
        #     'activity': forms.BooleanField(
        #         required=False
        #     )
        # }


class AddNewsForm(forms.Form):
    """
    Форма добавления новости
    """
    
    header = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': form_control_lg_mtb_3,
                'placeholder': 'Заголовок новости'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': form_control_lg_mtb_3,
                'rows': 5,
                'placeholder': 'Текст новости'
            }
        )
    )
    activity = forms.BooleanField(
        required=False,
        initial=True
    )
    
    class Meta:
        model = NewsItem


class AddCommentForm(forms.ModelForm):
    """
    Форма добавления комментария
    """
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': form_control_lg_mtb_3,
                'placeholder': 'Ваше имя'
            }
        ),
        # required=False
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': form_control_lg_mtb_3,
                'rows': 3,
                'placeholder': 'Текст комментария'
            }
        )
    )
    
    class Meta:
        model = Comment
        fields = ['name', 'text']
