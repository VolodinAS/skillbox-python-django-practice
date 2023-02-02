from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_news.models import NewsItem
from tests.utils.response_print import response_print


class TestAddNewsViewPost(TestCase):
    """
    Page /page_news_add/ - POST, добавление новости
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
        is_logged = self.client.login(username='test_username', password='test_password')
        
        if is_logged:
            test_user = User.objects.get(username='test_username')
            
            news_data = {
                'user': test_user,
                'header': 'test_news_header',
                'content': 'test_new_content',
                'tag': 'test_news_tag'
            }
            
            template_name = 'pages/news/my.html'
            url = reverse('page_news_add')
            response = self.client.post(url, news_data, follow=True)
            # response_print(response, url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, '<b>test_news_header</b>')


class TestNewsPublishPost(TestCase):
    """
    Page /newsmoder/publish - POST, одобрение новости
    """
    
    @classmethod
    def setUpTestData(cls):
        moderator = User.objects.create(
            username='moderator'
        )
        moderator.set_password('moderator')
        moderator.save()
        
        mod = Group.objects.create(name='Модераторы')
        reg = Group.objects.create(name='Зарегистрированные пользователи')
        ver = Group.objects.create(name='Верифицированные пользователи')
        
        user = User.objects.create(
            username='user'
        )
        user.set_password('user')
        user.save()
        
        cls.news_item = NewsItem.objects.create(
            header='test news header by user',
            content='test news content by user',
            tag='test news tag by user'
        )
        
        mod.user_set.add(moderator)
        ver.user_set.add(user)
    
    def test_main(self):
        is_logged = self.client.login(username='moderator', password='moderator')
        
        if is_logged:
            user = User.objects.get(username='user')
            
            url = reverse('page_news_moder_publish')
            response = self.client.get(url)
            # response_print(response, url)
            self.assertContains(response, 'Модерация новостей (1)')
            
            template_name = 'pages/moder/verify_news_list.html'
            url = reverse('page_news_moder_publish')
            response = self.client.post(url, {
                'news_id': self.news_item.id
            }, follow=True)
            # response_print(response, url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, 'Модерация новостей (0)')


class TestNewsItemViewPost(TestCase):
    """
    Page /<int:pk> - POST, добавление комментария
    """
    
    @classmethod
    def setUpTestData(cls):
        # moderator = User.objects.create(
        #     username='moderator'
        # )
        # moderator.set_password('moderator')
        # moderator.save()
        
        mod = Group.objects.create(name='Модераторы')
        reg = Group.objects.create(name='Зарегистрированные пользователи')
        ver = Group.objects.create(name='Верифицированные пользователи')
        
        user = User.objects.create(
            username='user'
        )
        user.set_password('user')
        user.save()
        
        cls.news_item = NewsItem.objects.create(
            header='test news header by user',
            content='test news content by user',
            tag='test news tag by user'
        )
        
        # mod.user_set.add(moderator)
        ver.user_set.add(user)
    
    def test_main(self):
        is_logged = self.client.login(username='user', password='user')
        
        if is_logged:
            user = User.objects.get(username='user')
            
            comment_data = {
                'user': user,
                'text': 'comment by user'
            }
            
            template_name = 'pages/news/detail.html'
            url = reverse('page_news_item', kwargs={'pk': self.news_item.pk})
            response = self.client.post(url, comment_data, follow=True)
            # response_print(response, url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, 'comment by user')


class TestTagSearchGet(TestCase):
    """
    Page /tagsearch - GET, поиск по тегу
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
            header='test news header by user',
            content='test news content by user',
            tag='simpletag'
        )
        
        # mod.user_set.add(moderator)
        ver.user_set.add(user)
    
    def test_main_tag_only(self):
        template_name = 'pages/news/tagsearch.html'
        url = reverse('page_tag_search')
        response = self.client.get(f'{url}?tag=simpletag')
        # response_print(response, url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, '<a href="/tagsearch?tag=simpletag">#simpletag</a>')
    
    def test_main_tag_and_date(self):
    
        is_logged = self.client.login(username='user', password='user')
        if is_logged:
            template_name = 'pages/news/tagsearch.html'
            url = reverse('page_tag_search')
            dater = self.news_item.create_at.strftime("%d.%m.%Y")
            response = self.client.get(f'{url}?tag=simpletag&dater={dater}')
            # response_print(response, url)
            
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, '<a href="/tagsearch?tag=simpletag">#simpletag</a>')
            self.assertContains(response, 'input type="text" name="dater" value="12.12.2022"')
