from django.test import TestCase
from django.urls import reverse


class TestBlogsListView(TestCase):
    """
    Page /blogs/
    """
    def test_main(self):
        template_name = 'pages/blog/index/index.html'
        url = reverse('page_blog_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Блоги | Django | Skillbox')


class TestBlogMyListView(TestCase):
    """
    Page /myblog/
    """
    def test_main(self):
        template_name = 'pages/blog/myblog/myblog.html'
        url = reverse('page_my_blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Мой блог | Django | Skillbox')


class TestBlogAddView(TestCase):
    """
    Page /blogs/add/
    """
    def test_main(self):
        template_name = 'pages/blog/add/add.html'
        url = reverse('page_blog_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Добавить блог | Django | Skillbox')


class TestBlogImportView(TestCase):
    """
    Page /blogs/import/
    """
    def test_main(self):
        template_name = 'pages/blog/add/import.html'
        url = reverse('page_blog_import')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)
        self.assertContains(response, 'Импорт блога | Django | Skillbox')
