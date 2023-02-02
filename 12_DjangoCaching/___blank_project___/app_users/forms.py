from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('Логин')
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _('Пароль'),
            }
        )
    )


class RegForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Логин')
            }
        )
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Пароль')
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Повторите пароль')
            }
        ),
        strip=False
    )
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Ваше имя')
            }
        )
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Ваша фамилия')
            }
        )
    )
    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Дата рождения')
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    city = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Город проживания')
            }
        ),
    )
    phone = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Телефон')
            }
        ),
    )
    captcha = forms.CharField(
        required=True,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Ответ')
            }
        ),
    )
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')


class EditProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Ваше имя')
            }
        )
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Ваша фамилия')
            }
        )
    )
    birthday = forms.DateField(
        required=True,
        label='Дата рождения',
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Дата рождения')
            }
        ),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    city = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Город проживания')
            }
        ),
    )
    phone = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Телефон')
            }
        ),
    )
    avatar_file = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'accept': '.jpg, .jpeg, .png, .gif'
            }
        )
    )
