import datetime
import time

from django.http import HttpRequest
from django.shortcuts import redirect
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
    
    main_header = 'Джановости'
    page_header = f'{main_header} | Django | Skillbox'
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
    
    main_header = 'Просмотр новости'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(NewsItemView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        add_comment_form = CommentForm()
        
        # context['ipaddress'] = self.request.META['REMOTE_ADDR']
        # context['add_comment_form'] = add_comment_form
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
                    context['msg'] = 'Комментарий добавлен!'
                    context['msg_theme'] = 'success'
                    return redirect('page_news_item', news_item.id)
                else:
                    context['msg'] = 'Ошибка при добавлении комментария...'
                    context['msg_theme'] = 'danger'
        
        else:
            context['msg'] = 'Вы должны авторизоваться, прежде чем писать комментарий'
            context['msg_theme'] = 'warning'
        
        context['form'] = add_comment_form
        
        return self.render_to_response(context=context)


class AddNewsView(TemplateView):
    template_name = 'pages/news/add.html'
    
    main_header = 'Добавить новость'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
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
        
        context['msg'] = 'Обработка...'
        
        form = NewsItemForm(request.POST)
        
        if request.user.is_authenticated:
            context['msg'] = 'Авторизация пройдена'
            if request.user.groups.filter(name='Верифицированные пользователи').exists() or request.user.groups.filter(
                    name='Модераторы').exists():
                context['msg'] = 'Права присутствуют'
                if form.is_valid():
                    context['msg'] = 'Форма валидная'
                    news = NewsItem.objects.create(
                        header=form.cleaned_data.get('header'),
                        content=form.cleaned_data.get('content'),
                        user=request.user,
                        tag=form.cleaned_data.get('tag'),
                    )
                    if news.id:
                        context['msg'] = 'Новость создана!'
                        return redirect('page_my_news')
                    else:
                        context['msg'] = 'Проблема с добавлением новости в БД'
            else:
                context['msg'] = 'У Вас нет прав на добавление новостей!'
        else:
            context['msg'] = 'Вы не авторизованы, чтобы добавлять новость!'
        
        context['form'] = form
        
        return self.render_to_response(context=context)


class MyNewsView(generic.ListView):
    """
   Страница новостей пользователя
    """
    
    model = NewsItem
    template_name = 'pages/news/my.html'
    # queryset = NewsItem.objects.all()
    
    main_header = 'Мои Джановости'
    page_header = f'{main_header} | Django | Skillbox'
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
    
    main_header = 'Редактирование новости'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(MyNewsDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title

        if self.request.user.is_authenticated:
            context['msg'] = 'Тут детали новости'
            context['msg_theme'] = 'success'
        else:
            context['msg'] = 'Вы не авторизованы, чтобы добавлять новость!'
            context['msg_theme'] = 'success'
        
        # add_comment_form = AddCommentForm()
        
        # context['ipaddress'] = self.request.META['REMOTE_ADDR']
        # context['add_comment_form'] = add_comment_form
        # context['id'] = NewsItem.
        
        return context
    
    # def post(self, request: HttpRequest, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = super(NewsDetails, self).get_context_data(**kwargs)
    #     print('IM POST HERE')
    #
    #     context['page_header'] = self.page_header
    #     context['page_title'] = self.page_title
    #
    #     news_item: NewsItem = self.get_object()
    #     # request.POST._mutable = True
    #     add_comment_form = AddCommentForm(request.POST)
    #
    #     form: Comment = add_comment_form.save(commit=False)
    #     form.news = news_item
    #
    #     if request.user.is_authenticated:
    #         form.user = request.user
    #         form.save()
    #         return HttpResponseRedirect(f'/news/{news_item.id}')
    #     else:
    #         if add_comment_form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect(f'/news/{news_item.id}')
    #
    #     context['add_comment_form'] = add_comment_form
    #
    #     return self.render_to_response(context=context)


class NewsModerListView(generic.ListView):
    """
   Страница новостей для модерации
    """
    
    model = NewsItem
    template_name = 'pages/moder/verify_news_list.html'
    # queryset = NewsItem.objects.all()
    queryset = NewsItem.objects.filter(published=False)
    
    main_header = 'Модерация новостей'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = main_header
    
    context_object_name = 'news_list_moder'
    
    # def get_queryset(self):
    #     queryset = super(NewsModerListView, self).get_queryset()
    #     queryset = queryset.filter(published=False)
    #     return queryset
    
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
    
    main_header = 'Модерирование новости'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(NewsModerDetailView, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        # add_comment_form = AddCommentForm()
        
        # context['ipaddress'] = self.request.META['REMOTE_ADDR']
        # context['add_comment_form'] = add_comment_form
        # context['id'] = NewsItem.
        
        return context
    
    # def post(self, request: HttpRequest, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = super(NewsDetails, self).get_context_data(**kwargs)
    #     print('IM POST HERE')
    #
    #     context['page_header'] = self.page_header
    #     context['page_title'] = self.page_title
    #
    #     news_item: NewsItem = self.get_object()
    #     # request.POST._mutable = True
    #     add_comment_form = AddCommentForm(request.POST)
    #
    #     form: Comment = add_comment_form.save(commit=False)
    #     form.news = news_item
    #
    #     if request.user.is_authenticated:
    #         form.user = request.user
    #         form.save()
    #         return HttpResponseRedirect(f'/news/{news_item.id}')
    #     else:
    #         if add_comment_form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect(f'/news/{news_item.id}')
    #
    #     context['add_comment_form'] = add_comment_form
    #
    #     return self.render_to_response(context=context)


class NewsPublish(TemplateView):
    template_name = 'pages/moder/verify_news_list.html'
    
    main_header = 'Модерация новостей'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
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
            context['msg'] = f'Новость <b>"{news.header}"</b> опубликована!'
        else:
            context['msg'] = 'Не указан ID новости!'
        
        context['news_list_moder'] = news_list_moder
        return redirect('/newsmoder/', context=context)
        
        # return self.render_to_response(context=context)


class TagSearch(TemplateView):
    template_name = 'pages/news/tagsearch.html'
    
    main_header = 'Поиск по тегу'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
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
