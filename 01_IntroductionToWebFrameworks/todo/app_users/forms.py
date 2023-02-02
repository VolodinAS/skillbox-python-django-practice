from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Логин'
            }
        ),
        label='Логин:'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Пароль',
            }
        ),
        label='Пароль:'
    )


class RegForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=False,
        # help_text='Имя',
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        # help_text='Фамилия',
        label='Фамилия'
    )
    birthday = forms.DateField(
        required=True,
        label='Дата рождения'
    )
    city = forms.CharField(
        required=False,
        max_length=50,
        label='Город проживания'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
