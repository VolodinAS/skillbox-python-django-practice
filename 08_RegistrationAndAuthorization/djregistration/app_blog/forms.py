from django import forms


class BlogAddForm(forms.Form):
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
                'placeholder': 'Текст блога, 5000 символов',
                'rows': 5
            }
        )
    )
    images = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True,
                # 'class': 'custom-file-input',
                # 'accept': '.jpg, .jpeg, .png, .gif'
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
