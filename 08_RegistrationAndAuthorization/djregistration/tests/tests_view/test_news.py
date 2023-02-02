from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_news.models import NewsItem


class TestNewsIndex(TestCase):
    """
    Page /
    """
    
    def test_main(self):
        template_name = 'pages/news/index.html'
        url = reverse('page_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Джановости | Django | Skillbox')


class TestNewsItemView(TestCase):
    """
    Page /<int:pk>
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username',
            password='test_password'
        )
        cls.news_item = NewsItem.objects.create(
            header='test header',
            content='test content',
            user=test_user
        )
    
    def test_main(self):
        template_name = 'pages/news/detail.html'
        url = reverse('page_news_item', kwargs={'pk': self.news_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Просмотр новости | Django | Skillbox')
    
    def test_main(self):
        template_name = 'pages/news/detail.html'
        url = reverse('page_news_item', kwargs={'pk': self.news_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Просмотр новости | Django | Skillbox')


class TestAddNewsView(TestCase):
    """
    Page /news/add/
    """
    
    def test_main(self):
        template_name = 'pages/news/add.html'
        url = reverse('page_news_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Добавить новость | Django | Skillbox')


class TestMyNewsView(TestCase):
    """
    Page /mynews/
    """
    
    def test_main(self):
        template_name = 'pages/news/my.html'
        url = reverse('page_my_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Мои Джановости | Django | Skillbox')


class TestMyNewsDetailView(TestCase):
    """
    Page /mynews/<int:pk>
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
        cls.news_item = NewsItem.objects.create(
            header='test header',
            content='test content',
            user=user
        )
        ver.user_set.add(user)
    
    def test_main(self):
        template_name = 'pages/news/my_detail.html'
        url = reverse('page_my_news_detail', kwargs={'pk': self.news_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Редактирование новости | Django | Skillbox')
    
    def test_main_tag_and_date(self):
        is_logged = self.client.login(username='user', password='user')
        # print(f'{is_logged=}')
        if is_logged:
            template_name = 'pages/news/my_detail.html'
            url = reverse('page_my_news_detail', kwargs={'pk': self.news_item.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, 'Редактирование новости | Django | Skillbox')


class TestNewsModerListView(TestCase):
    """
    Page /newsmoder/
    """
    
    def test_main(self):
        template_name = 'pages/moder/verify_news_list.html'
        url = reverse('page_news_moder')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Модерация новостей | Django | Skillbox')


class TestNewsModerDetailView(TestCase):
    """
    Page /newsmoder/<int:pk>
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username',
            password='test_password'
        )
        
        cls.news_item = NewsItem.objects.create(
            header='test header',
            content='test content',
            user=test_user
        )
    
    def test_main(self):
        template_name = 'pages/news/my_detail.html'
        url = reverse('page_my_news_detail_moder', kwargs={'pk': self.news_item.pk})
        
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Модерирование новости')


class TestNewsPublish(TestCase):
    """
    Page /newsmoder/publish
    """
    
    def test_main(self):
        template_name = 'pages/moder/verify_news_list.html'
        url = reverse('page_news_moder_publish')
        response = self.client.get(url)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Нужна авторизация')


class TestTagSearch(TestCase):
    """
    Page /tagsearch
    """
    
    def test_main(self):
        template_name = 'pages/news/tagsearch.html'
        url = reverse('page_tag_search')
        response = self.client.get(url)
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Поиск по тегу | Django | Skillbox')
