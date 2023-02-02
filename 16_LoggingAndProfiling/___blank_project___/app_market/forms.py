from django import forms


class CartAddProductForm(forms.Form):
    """
    Форма добавления товара в корзину
    """
    quantity = forms.CharField(
        initial=1,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Количество'
            }
        )
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)