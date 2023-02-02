from _csv import reader

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.shortcuts import redirect
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
    
    main_header = 'Блоги'
    page_header = f'{main_header} | Django | Skillbox'
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
    
    main_header = 'Мой блог'
    page_header = f'{main_header} | Django | Skillbox'
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
    
    main_header = 'Читать блог'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class BlogAddView(generic.TemplateView):
    template_name = 'pages/blog/add/add.html'
    
    main_header = 'Добавить блог'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
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
                    context['msg'] = 'Проблема при создании блога!'
                    context['msg_theme'] = 'warning'
            
            context['form'] = blog_add_form
        else:
            context['msg'] = 'Вы должны авторизоваться, прежде чем писать комментарий'
            context['msg_theme'] = 'warning'
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return self.render_to_response(context=context)


class BlogImportView(generic.TemplateView):
    template_name = 'pages/blog/add/import.html'
    
    main_header = 'Импорт блога'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'Импортировать блоги из CSV-файла'
    
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
                
                # print(f'{csv_files_files=}')
                # print(f'{csv_files_form=}')
                
                # print(f'{len(csv_files_files)=}')
                total_files = len(csv_files_files)
                if total_files > 0:
                    csv_file: InMemoryUploadedFile
                    
                    load_files = 0
                    for csv_file in csv_files_files:
                        # logger.info(f'Начинаю парсинг файла {csv_file}')
                        csv_file_data = csv_file.read()
                        is_decode = False
                        csv_file_str: str
                        try:
                            csv_file_str = csv_file_data.decode('utf-8').split('\n')
                        except UnicodeDecodeError:
                            try:
                                csv_file_str = csv_file_data.decode('cp1251').split('\n')
                            except UnboundLocalError:
                                context['msg'] = 'Кодировка файла не распознана'
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
                                            blog_import_form.add_error(None,
                                                                       f'В файле {csv_file} дата публикации должна быть в формате "дд.мм.гггг чч:мм"')
                                        else:
                                            # print('='*50)
                                            # print(f'{header=}')
                                            # print(f'{content=}')
                                            # print(f'{date=}')
                                            # print('='*50)
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
                                                        # logger.debug(f'Блог "{header}" импортирован!')
                                                    else:
                                                        blog_import_form.add_error(None,
                                                                                   f'Проблема с добавлением файла блога "{header}" из файла {csv_file}!')
                                                else:
                                                    blog_import_form.add_error(None,
                                                                               f'В файле {csv_file} длина контента должна быть от 1 до 5000 символов ')
                                            else:
                                                blog_import_form.add_error(None,
                                                                           f'В файле {csv_file} длина заголовка должна быть от 1 до 200 символов ')
                                    else:
                                        blog_import_form.add_error(None,
                                                                   f'В файле {csv_file} дата публикации должна быть в формате "дд.мм.гггг чч:мм"')
                            load_files += 1
                        # logger.info(f'Закончил парсинг файла {csv_file}')
                    # logger.debug(f'Обработанных файлов: {load_files}')
                    # logger.debug(f'Всего файлов: {total_files}')
                    if load_files == total_files:
                        # logger.success('Блоги успешно загружены!')
                        return redirect('page_my_blog')
                    else:
                        context['msg'] = 'Что-то пошло не так при импорте файлов...'
                        context['msg_theme'] = 'warning'
                else:
                    context['msg'] = 'Нет загружаемых файлов'
                    context['msg_theme'] = 'warning'
            
            else:
                context['msg'] = blog_import_form.errors
                context['msg_theme'] = 'warning'
            context['form'] = blog_import_form
        else:
            context['msg'] = 'Вы должны авторизоваться, прежде чем писать комментарий'
            context['msg_theme'] = 'warning'
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        return self.render_to_response(context=context)
