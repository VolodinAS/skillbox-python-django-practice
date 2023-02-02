from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_users.models import Profile
from tests.utils.fake_upload_files import get_fake_file
from tests.utils.get_upload_by_path import get_upload_by_path
from tests.utils.response_print import response_print


class TestLoginPost(TestCase):
    """
    Page /login/ - POST, авторизация
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        Group.objects.create(name='Модераторы')
        # Group.objects.create(name='Зарегистрированные пользователи')
        
        group = Group.objects.get(name='Модераторы')
        group.user_set.add(test_user)
    
    def test_main(self):
        auth_data = {
            'username': 'test_username',
            'password': 'test_password'
        }
        
        template_name = 'auth_template/index.html'
        url = reverse('auth_login')
        response = self.client.post(url, auth_data, follow=True)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, '<b>test_username</b>')


class TestRegPost(TestCase):
    """
    Page /reg/ - POST, регистрация
    """
    
    @classmethod
    def setUpTestData(cls):
        group_name = 'Зарегистрированные пользователи'
        group = Group(name=group_name)
        group.save()
        group_name = 'Модераторы'
        group = Group(name=group_name)
        group.save()
    
    # @tag('failure')
    def test_main(self):
        # logger.info('TestRegPost > test_main')
        url = reverse('auth_reg')
        self.client.get(url)
        session = self.client.session
        reg_data = {
            'username': 'test_username',
            'password1': 'test_password',
            'password2': 'test_password',
            'birthday': '12.12.1992',
            'captcha': session['summa'],
        }
        
        template_name = 'auth_template/index.html'
        url = reverse('auth_reg')
        response = self.client.post(url, reg_data, follow=True)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, '<b>test_username</b>')
        new_user = User.objects.filter(username='test_username')
        self.assertTrue(new_user.exists())
        new_user = User.objects.get(username='test_username')
        self.assertTrue(Profile.objects.filter(user=new_user).exists())


class TestUserProfilePost(TestCase):
    """
    Page /profile - POST - сохранение профиля
    """
    
    @classmethod
    def setUpTestData(cls):
        mod = Group.objects.create(name='Модераторы')
        reg = Group.objects.create(name='Зарегистрированные пользователи')
        ver = Group.objects.create(name='Верифицированные пользователи')
        
        user = User.objects.create(
            username='user'
        )
        user.set_password('user')
        user.save()
        
        reg.user_set.add(user)
    
    def test_main(self):
        is_logged = self.client.login(username='user', password='user')
        
        if is_logged:
            user = User.objects.get(username='user')
            
            avatar_image = get_fake_file('avatar.jpg')
            if avatar_image:
                avatar_file = get_upload_by_path(
                    path=avatar_image,
                    file_name='avatar.jpg',
                    file_type='image/jpeg'
                )
                
                profile_data = {
                    'birthday': '12.12.1992',
                    'avatar_file': avatar_file
                }
                
                template_name = 'profile/index.html'
                url = reverse('user_profile')
                response = self.client.post(url, profile_data, follow=True)
                # response_print(response, url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertContains(response, 'Профиль успешно обновлён')
