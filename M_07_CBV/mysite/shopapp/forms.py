from django.contrib.auth.models import Group
from django.forms import models


class GroupForm(models.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
