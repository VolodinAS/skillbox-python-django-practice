from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from app_users.models import User


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    date_of_birth = forms.DateField(required=False, help_text='Дата рождения',
                                    widget=SelectDateWidget(years=range(1910, 2020)))
    city = forms.CharField(max_length=30, required=False, help_text='Город')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    file = forms.FileField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()

