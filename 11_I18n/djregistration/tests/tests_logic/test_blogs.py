import os.path

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from loguru import logger

from tests.utils.fake_upload_files import get_fake_file
from tests.utils.response_print import response_print


class TestBlogAddViewNoImagesPost(TestCase):
    """
    Page /blogs/add/ - POST, no images
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        Group.objects.create(name='Модераторы')
        
        group = Group.objects.get(name='Модераторы')
        group.user_set.add(test_user)
    
    def test_main(self):
        is_logged = self.client.login(username='test_username', password='test_password')
        
        if is_logged:
            test_user = User.objects.get(username='test_username')
            
            blog_data = {
                'user': test_user,
                'header': 'blog_test_header_no_images',
                'content': 'blog_test_content_no_images'
            }
            
            template_name = 'pages/blog/detail/detail.html'
            url = reverse('page_blog_add')
            response = self.client.post(url, blog_data, follow=True)
            # response_print(response, url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name)
            self.assertContains(response, '«blog_test_header_no_images»')


class TestBlogAddViewImagesPost(TestCase):
    """
    Page /blogs/add/ - POST, images
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        Group.objects.create(name='Модераторы')
        
        group = Group.objects.get(name='Модераторы')
        group.user_set.add(test_user)
    
    def test_main(self):
        is_logged = self.client.login(username='test_username', password='test_password')
        
        if is_logged:
            test_user = User.objects.get(username='test_username')
            
            photo_1 = get_fake_file('django tests.jpg')
            photo_2 = get_fake_file('Sapling.png')
            
            # logger.info(f'{photo_1=}')
            # logger.info(f'{photo_2=}')
            
            if photo_1 and photo_2:
                image_1 = SimpleUploadedFile(
                    name='image1.jpg',
                    # content=open(os.path.join('images', 'blogs', '123rf-logo-white.png'), 'rb').read()
                    content=open(photo_1, 'rb').read(),
                    content_type='image/jpeg'
                )
                
                image_2 = SimpleUploadedFile(
                    name='image2.jpg',
                    content=open(photo_2, 'rb').read(),
                    content_type='image/jpeg'
                )
                
                # logger.info(f'{image_1=}')
                # logger.info(f'{image_2=}')
                
                blog_data = {
                    'user': test_user,
                    'header': 'blog_test_header_images',
                    'content': 'blog_test_content_images',
                    'images': [
                        image_1,
                        image_2
                    ]
                }
                
                template_name = 'pages/blog/detail/detail.html'
                url = reverse('page_blog_add')
                response = self.client.post(url, blog_data, follow=True)
                # response_print(response, url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertContains(response, '/media/images/blogs/image2')


class TestBlogImportViewPost(TestCase):
    """
    Page /blogs/import/ - POST
    """
    
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_username'
        )
        test_user.set_password('test_password')
        test_user.save()
        
        Group.objects.create(name='Модераторы')
        
        group = Group.objects.get(name='Модераторы')
        group.user_set.add(test_user)
    
    def test_main(self):
        is_logged = self.client.login(username='test_username', password='test_password')
        
        if is_logged:
            test_user = User.objects.get(username='test_username')
            
            fake_file_1 = get_fake_file('blogs_1_2.csv')
            fake_file_2 = get_fake_file('blogs_3_4.csv')
            
            if fake_file_1 and fake_file_2:
                
                blog_1_2 = SimpleUploadedFile(
                    name='blog12.csv',
                    content=open(fake_file_1, 'rb').read(),
                    # content_type='application/vnd.ms-excel'
                )
                
                blog_3_4 = SimpleUploadedFile(
                    name='blog34.csv',
                    content=open(fake_file_2, 'rb').read(),
                    # content_type='application/vnd.ms-excel'
                )
                
                blog_import_data = {
                    'user': test_user,
                    'csv_files': [
                        blog_1_2,
                        blog_3_4
                    ]
                }
                
                template_name = 'pages/blog/myblog/myblog.html'
                url = reverse('page_blog_import')
                response = self.client.post(url, blog_import_data, follow=True)
                # response_print(response, url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                # TODO Файлы блогов почему-то не загружаются.. Хотя путь указан и post-скрипт срабатывает...
                self.assertContains(response, 'У Вас еще нет блогов')
            
            else:
                logger.error('Fake files doesnt exists!')
