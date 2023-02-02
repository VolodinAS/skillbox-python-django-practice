from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    city = models.CharField(
        max_length=50,
        blank=True
    )
    birthday = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} ({self.birthday}) - {self.city}'
