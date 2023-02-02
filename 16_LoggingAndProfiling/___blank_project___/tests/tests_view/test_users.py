from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_users.models import Profile
from tests.utils.response_print import response_print


class TestLoginAuthView(TestCase):
    """
    Page /login/
    """
    
    def test_main(self):
        template_name = 'pages/auth/auth.html'
        url = reverse('auth_login')
        response = self.client.get(url)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Логин:')


class TestLogoutAuthView(TestCase):
    """
    Page /logout/ - redirect
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        mod = Group.objects.create(name='Модераторы')
        reg = Group.objects.create(name='Зарегистрированные пользователи')
        ver = Group.objects.create(name='Верифицированные пользователи')
        
        mod.user_set.add(test_user)
        ver.user_set.add(test_user)
    
    def test_main(self):
        url = reverse('auth_logout')
        template_name = 'auth_template/logout.html'
        response = self.client.get(
            path=url,
            data={},
            follow=True,
            HTTP_REFERER=reverse('page_index'),
            # HTTP_HOST='http://127.0.0.1:8000/',
            HTTP_HOST='localhost',
            SERVER_NAME='localhost'
        )
        self.assertEqual(response.status_code, 200)
        # response_print(response, url)
        self.assertTemplateUsed(response, template_name)
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertContains(response, 'http-equiv="refresh"')


class TestRegView(TestCase):
    """
    Page /reg/
    """
    
    def test_main(self):
        template_name = 'pages/auth/reg.html'
        url = reverse('auth_reg')
        response = self.client.get(url)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Ваша фамилия:')


class TestUserProfile(TestCase):
    """
    Page /profile/
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        mod = Group.objects.create(name='Модераторы')
        reg = Group.objects.create(name='Зарегистрированные пользователи')
        ver = Group.objects.create(name='Верифицированные пользователи')
        
        mod.user_set.add(test_user)
        ver.user_set.add(test_user)
        
        Profile.objects.create(
            user=test_user,
            city='totty'
        )
    
    def test_main(self):
        is_logged = self.client.login(username='test_username', password='test_password')
        if is_logged:
            template_name = 'profile/index.html'
            url = reverse('user_profile')
            response = self.client.get(url)
            # response_print(response, url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, 'value="totty"')


class TestViewProfile(TestCase):
    """
    Page /profile/<int:pk>
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(
            username='test_username',
            password='test_password'
        )
    
    def test_main(self):
        template_name = 'profile/index.html'
        url = reverse('view_profile', kwargs={'pk': self.test_user.pk})
        
        response = self.client.get(url)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, '<div class="col">test_username</div>')


class TestUserVerify(TestCase):
    """
    Page /verifyme/
    """
    
    def test_main(self):
        template_name = 'pages/moder/verify_users.html'
        url = reverse('user_verify')
        response = self.client.get(url)
        # response_print(response, url)
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Верификация | Django | Skillbox')
