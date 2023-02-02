from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('tid_models_blog_user')  # 'Чей профиль (AbstractUser)'
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('tid_form_labels_reg_city'),  # 'Город проживания'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('tid_form_labels_reg_birthday'),  # 'Дата рождения'
    )
    phone = models.CharField(
        max_length=30,
        verbose_name=_('tid_form_labels_reg_phone'),  # 'Телефон'
    )
    avatar_file = models.ImageField(
        upload_to='images/user_avatars/',
        null=True,
        blank=True
        # upload_to=path_and_rename("images/user_avatars/")
    )
    
    def __str__(self):
        return f'{self.user.username}, ({self.birthday})'
    
    class Meta:
        verbose_name = _('tid_models_profiles_meta_vn')  # 'профиль'
        verbose_name_plural = _('tid_models_profiles_meta_vnp')  # 'профили'
        db_table = 'profile'
        ordering = ['id']
