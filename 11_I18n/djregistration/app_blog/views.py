from _csv import reader

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic
from loguru import logger

from app_blog.forms import BlogAddForm
from app_blog.forms import BlogImportForm
from app_blog.models import Blog
from app_blog.models import BlogImages
from utils.date_and_unix import date_string_to_unix_by_format


class BlogsListView(generic.ListView):
    template_name = 'pages/blog/index/index.html'
    model = Blog
    context_object_name = 'blog_list'
    
    main_header = _('tid_headermenu_blogs')
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(BlogsListView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class BlogMyListView(generic.ListView):
    template_name = 'pages/blog/myblog/myblog.html'
    model = Blog
    context_object_name = 'blog_list'
    queryset = Blog.objects.all()
    
    main_header = _('tid_headermenu_profile_my_blog')  # 'Мой блог'
    page_header = main_header
    page_title = main_header
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super(BlogMyListView, self).get_queryset()
            queryset = queryset.filter(user=self.request.user)
            return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(BlogMyListView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'pages/blog/detail/detail.html'
    context_object_name = 'blog_item'
    
    main_header = _('tid_views_blog_read')  # 'Читать блог'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class BlogAddView(generic.TemplateView):
    template_name = 'pages/blog/add/add.html'
    
    main_header = _('tid_buttons_blog_add')  # 'Добавить блог'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        blog_add_form = BlogAddForm()
        
        context['form'] = blog_add_form
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if request.user.is_authenticated:
            blog_add_form = BlogAddForm(request.POST, request.FILES)
            
            if blog_add_form.is_valid():
                # print(request.FILES)
                new_blog: Blog = Blog.objects.create(
                    header=blog_add_form.cleaned_data.get('header'),
                    content=blog_add_form.cleaned_data.get('content'),
                    user=request.user
                )
                if new_blog.id:
                    # print(request.FILES)
                    images_data = request.FILES.getlist('images')
                    for img in images_data:
                        instance_img = BlogImages(
                            blog=new_blog,
                            image=img
                        )
                        instance_img.save()
                    
                    return redirect('page_blog_detail', new_blog.id)
                
                else:
                    context['msg'] = _('tid_messages_system_views_blogs_mysql')  # 'Проблема при создании блога!'
                    context['msg_theme'] = 'warning'
            
            context['form'] = blog_add_form
        else:
            context['msg'] = _('tid_messages_news_comment_denied')  # 'Вы должны авторизоваться, прежде чем писать комментарий'
            context['msg_theme'] = 'warning'
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return self.render_to_response(context=context)


class BlogImportView(generic.TemplateView):
    template_name = 'pages/blog/add/import.html'
    
    main_header = _('tid_buttons_blogs_import')  # 'Импорт блога'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        blog_import_form = BlogImportForm()
        
        context['form'] = blog_import_form
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if request.user.is_authenticated:
            blog_import_form = BlogImportForm(request.POST, request.FILES)
            
            if blog_import_form.is_valid():
                csv_files_files = request.FILES.getlist('csv_files')
                csv_files_form = blog_import_form.cleaned_data['csv_files']
                total_files = len(csv_files_files)
                if total_files > 0:
                    csv_file: InMemoryUploadedFile
                    
                    load_files = 0
                    for csv_file in csv_files_files:
                        csv_file_data = csv_file.read()
                        is_decode = False
                        csv_file_str: str
                        try:
                            csv_file_str = csv_file_data.decode('utf-8').split('\n')
                        except UnicodeDecodeError:
                            try:
                                csv_file_str = csv_file_data.decode('cp1251').split('\n')
                            except UnboundLocalError:
                                context['msg'] = _('tid_messages_system_views_blogs_import_encode')  # 'Кодировка файла не распознана'
                                context['msg_theme'] = 'warning'
                            else:
                                is_decode = True
                        else:
                            is_decode = True
                        
                        if is_decode:
                            csv_reader = reader(csv_file_str, delimiter=';')
                            for row in csv_reader:
                                if len(row) == 3:
                                    header, content, dater = row
                                    if len(dater):
                                        try:
                                            date = date_string_to_unix_by_format(dater, '%d.%m.%Y %H:%M')
                                        except ValueError:
                                            blog_import_form.add_error(
                                                None,
                                                _('tid_messages_system_views_blogs_import_date')  # f'В файле {csv_file} дата публикации должна быть в формате "дд.мм.гггг чч:мм"'
                                            )
                                        else:
                                            if 1 < len(header) <= 200:
                                                if 1 < len(content) <= 5000:
                                                    new_blog = Blog.objects.create(
                                                        header=header,
                                                        content=content,
                                                        user=request.user
                                                    )
                                                    if new_blog.id:
                                                        new_blog.create_at = date
                                                        new_blog.save()
                                                    else:
                                                        blog_import_form.add_error(
                                                            None,
                                                            _('tid_messages_system_views_blogs_import_item')  # f'Проблема с добавлением файла блога "{header}" из файла {csv_file}!'
                                                        )
                                                else:
                                                    blog_import_form.add_error(
                                                        None,
                                                        _('tid_messages_system_views_blogs_import_text')  # f'В файле {csv_file} длина контента должна быть от 1 до 5000 символов '
                                                    )
                                            else:
                                                blog_import_form.add_error(
                                                    None,
                                                    _('tid_messages_system_views_blogs_import_header')  # f'В файле {csv_file} длина заголовка должна быть от 1 до 200 символов '
                                                )
                                    else:
                                        blog_import_form.add_error(
                                            None,
                                            _('tid_messages_system_views_blogs_import_date')  # f'В файле {csv_file} дата публикации должна быть в формате "дд.мм.гггг чч:мм"'
                                        )
                            load_files += 1
                            
                    if load_files == total_files:
                        return redirect('page_my_blog')
                    else:
                        context['msg'] = _('tid_messages_system_views_blogs_import_error')  # 'Что-то пошло не так при импорте файлов...'
                        context['msg_theme'] = 'warning'
                else:
                    context['msg'] = _('tid_messages_system_views_blogs_import_no_files')  # 'Нет загружаемых файлов'
                    context['msg_theme'] = 'warning'
            
            else:
                context['msg'] = blog_import_form.errors
                context['msg_theme'] = 'warning'
            context['form'] = blog_import_form
        else:
            context['msg'] = _('tid_messages_blogs_import_auth')  # 'Вы должны авторизоваться, прежде чем импортировать блоги'
            context['msg_theme'] = 'warning'
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return self.render_to_response(context=context)
