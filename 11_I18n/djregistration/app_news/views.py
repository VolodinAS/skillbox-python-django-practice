import datetime
import time

from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import TemplateView

from app_comments.forms import CommentForm
from app_comments.models import Comment
from .forms import NewsItemForm
from .forms import SearchTag
from .models import NewsItem


class NewsIndex(generic.ListView):
    """
    Индекс-страница новостей
    """
    
    model = NewsItem
    template_name = 'pages/news/index.html'
    
    main_header = _('tid_headermenu_news')  # 'Джановости'
    page_header = main_header
    page_title = main_header
    
    context_object_name = 'news_list'
    queryset = NewsItem.objects.filter(published=True)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(NewsIndex, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class NewsItemView(generic.DetailView):
    model = NewsItem
    template_name = 'pages/news/detail.html'
    context_object_name = 'news_item'
    
    main_header = _('tid_views_news_item_read')  # 'Просмотр новости'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super(NewsItemView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        add_comment_form = CommentForm()
        
        context['form'] = add_comment_form
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = super(NewsItemView, self).get_context_data(**kwargs)
        # print('IM POST HERE')
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        #
        news_item: NewsItem = self.get_object()
        
        # print(f'{news_item=}')
        
        add_comment_form: CommentForm = CommentForm(request.POST)
        
        if request.user.is_authenticated:
            if add_comment_form.is_valid():
                text = add_comment_form.cleaned_data.get('text')
                
                new_comment: Comment = Comment.objects.create(
                    news=news_item,
                    user=request.user,
                    text=text
                )
                if new_comment.id:
                    context['msg'] = _('tid_views_news_item_comment_add')  # 'Комментарий добавлен!'
                    context['msg_theme'] = 'success'
                    return redirect('page_news_item', news_item.id)
                else:
                    context['msg'] = _('tid_views_news_item_comment_error')  # 'Ошибка при добавлении комментария...'
                    context['msg_theme'] = 'danger'
        
        else:
            context['msg'] = _('tid_messages_news_comment_denied')  # 'Вы должны авторизоваться, прежде чем писать комментарий'
            context['msg_theme'] = 'warning'
        
        context['form'] = add_comment_form
        
        return self.render_to_response(context=context)


class AddNewsView(TemplateView):
    template_name = 'pages/news/add.html'
    
    main_header = _('tid_buttons_news_add')  # 'Добавить новость'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        context['form'] = NewsItemForm()
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        form = NewsItemForm(request.POST)
        
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Верифицированные пользователи').exists() or request.user.groups.filter(
                    name='Модераторы').exists():
                if form.is_valid():
                    news = NewsItem.objects.create(
                        header=form.cleaned_data.get('header'),
                        content=form.cleaned_data.get('content'),
                        user=request.user,
                        tag=form.cleaned_data.get('tag'),
                    )
                    if news.id:
                        return redirect('page_my_news')
                    else:
                        context['msg'] = _('tid_views_add_news_mysql')  # 'Проблема с добавлением новости в БД'
            else:
                context['msg'] = _('tid_messages_news_list_denied')  # 'У Вас нет прав на добавление новостей!'
        else:
            context['msg'] = _('tid_messages_system_need_auth')  # 'Вы не авторизованы, чтобы добавлять новость!'
        
        context['form'] = form
        
        return self.render_to_response(context=context)


class MyNewsView(generic.ListView):
    """
   Страница новостей пользователя
    """
    
    model = NewsItem
    template_name = 'pages/news/my.html'
    # queryset = NewsItem.objects.all()
    
    main_header = _('tid_headermenu_profile_my_news')  # 'Мои Джановости'
    page_header = main_header
    page_title = main_header
    
    context_object_name = 'news_list'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super(MyNewsView, self).get_queryset()
            queryset = queryset.filter(user=self.request.user)
            return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(MyNewsView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class MyNewsDetailView(generic.DetailView):
    """
    Редактирование моей новости
    """
    
    model = NewsItem
    template_name = 'pages/news/my_detail.html'
    context_object_name = 'news_item'
    
    main_header = _('tid_views_news_edit_title')  # 'Редактирование новости'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super(MyNewsDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        if self.request.user.is_authenticated:
            context['msg'] = _('tid_views_news_edit_info')  # 'Тут детали новости'
            context['msg_theme'] = 'success'
        else:
            context['msg'] = _('tid_messages_system_need_auth')  # 'Вы не авторизованы, чтобы добавлять новость!'
            context['msg_theme'] = 'success'
        
        return context


class NewsModerListView(generic.ListView):
    """
   Страница новостей для модерации
    """
    
    model = NewsItem
    template_name = 'pages/moder/verify_news_list.html'
    # queryset = NewsItem.objects.all()
    queryset = NewsItem.objects.filter(published=False)
    
    main_header = _('tid_views_news_moder_title')  # 'Модерация новостей'
    page_header = main_header
    page_title = main_header
    
    context_object_name = 'news_list_moder'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(NewsModerListView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class NewsModerDetailView(generic.DetailView):
    """
    Редактирование моей новости
    """
    
    model = NewsItem
    template_name = 'pages/news/my_detail.html'
    context_object_name = 'news_item'
    
    main_header = _('tid_views_news_moder_title_item')  # 'Модерирование новости'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, **kwargs):
        context = super(NewsModerDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class NewsPublish(TemplateView):
    template_name = 'pages/moder/verify_news_list.html'
    
    main_header = _('tid_views_news_moder_title_publish')  # 'Публикация новости'
    page_header = main_header
    page_title = main_header
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        news_id = request.POST['news_id']
        
        news_list_moder = NewsItem.objects.filter(published=False)
        
        # print(f'{news_id=}')
        
        news = NewsItem.objects.get(id=news_id)
        if news.id:
            news.published = True
            news.published_by = request.user
            news.publicised_at = datetime.datetime.now()
            news.save()
            context['msg'] = _('tid_views_news_moder_publish_success')  # f'Новость <b>"{news.header}"</b> опубликована!'
        else:
            context['msg'] = _('tid_views_news_moder_publish_error')  # 'Не указан ID новости!'
        
        context['news_list_moder'] = news_list_moder
        return redirect('/newsmoder/', context=context)
        
        # return self.render_to_response(context=context)


class TagSearch(TemplateView):
    template_name = 'pages/news/tagsearch.html'
    
    main_header = _('tid_tag_search_form_label')  # 'Поиск по тегу'
    page_header = main_header
    page_title = main_header
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        tag = self.request.GET.get('tag', '')
        tag_form = SearchTag(self.request.GET)
        
        context['result'] = []
        
        if len(tag):
            search_result = NewsItem.objects.filter(tag=tag)
            
            date = self.request.GET.get('dater', '')
            
            # print(f'{date=}')
            
            if len(date):
                date_unix = int(time.mktime(datetime.datetime.strptime(date, "%d.%m.%Y").timetuple()))
                # date_unix += 86399  # 23.59.59
                date_from = datetime.datetime.fromtimestamp(date_unix)
                date_to = datetime.datetime.now()
                # print(f'{date_unix=}')
                # print(f'{date_from=}')
                search_result = search_result.filter(create_at__range=[date_from, date_to])
            
            context['result'] = search_result
        else:
            tag_form = SearchTag()
        
        context['form'] = tag_form
        
        return context
