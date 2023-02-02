from django.apps import apps
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.views import generic

from .forms import AddCommentForm
from .forms import AddNewsForm
from .forms import EditNewsForm
from .models_dir import Comment
from .models_dir import NewsItem


class Index(generic.ListView):
    """
    Индекс-страница новостей
    """
    
    model = NewsItem
    template_name = 'news_index/index.html'
    
    main_header = 'Новости'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = main_header
    
    context_object_name = 'news_list'
    queryset = NewsItem.objects.filter(activity=True)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(Index, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class NewsDetails(generic.DetailView):
    """
    Подробнее о новости
    """
    
    model = NewsItem
    template_name = 'news_details/index.html'
    context_object_name = 'news_item'
    
    main_header = 'Подробнее о новости'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(NewsDetails, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        add_comment_form = AddCommentForm()
        
        # context['ipaddress'] = self.request.META['REMOTE_ADDR']
        context['add_comment_form'] = add_comment_form
        # context['id'] = NewsItem.
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = super(NewsDetails, self).get_context_data(**kwargs)
        # print('IM POST HERE')
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        news_item: NewsItem = self.get_object()
        # request.POST._mutable = True
        add_comment_form = AddCommentForm(request.POST)
        
        form: Comment = add_comment_form.save(commit=False)
        form.news = news_item
        
        if request.user.is_authenticated:
            form.user = request.user
            form.save()
            return HttpResponseRedirect(f'/news/{news_item.id}')
        else:
            if add_comment_form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/news/{news_item.id}')
        
        context['add_comment_form'] = add_comment_form
        
        return self.render_to_response(context=context)


class EditNewsItem(generic.DetailView):
    """
    Страница с формой редактирования
    """
    
    model = NewsItem
    template_name = 'news_edit/index.html'
    context_object_name = 'news_item'
    
    main_header = 'Редактировать новость'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(EditNewsItem, self).get_context_data(**kwargs)
        
        pk = self.kwargs.get('pk', 0)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        news_item_edit: NewsItem = NewsItem.objects.get(pk=pk)
        news_edit_form = EditNewsForm(instance=news_item_edit)
        context['news_edit_form'] = news_edit_form
        # context['form'] = EditNewsForm(initial={'post': news_edit_form})
        
        # print(f'{news_item_edit=}')
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        context = super(EditNewsItem, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        news_edit_form = EditNewsForm(request.POST)
        
        pk = self.kwargs.get('pk', 0)
        # print(f'{pk=}')
        
        # print(f'{news_edit_form.is_valid()=}')
        
        news_item = NewsItem.objects.get(pk=pk)
        news_item_form = EditNewsForm(request.POST, instance=news_item)
        
        if news_item_form.is_valid():
            news_item.save()
            
            return HttpResponseRedirect(f'/news/{pk}')
        
        context['news_edit_form'] = news_item_form
        
        return self.render_to_response(context=context)


class AddNews(generic.TemplateView):
    """
    Страница с формой добавления новости
    """
    
    template_name = 'news_add/index.html'
    
    main_header = 'Добавить новость'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(AddNews, self).get_context_data(**kwargs)
        
        add_news_form = AddNewsForm()
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        context['add_news_form'] = add_news_form
        
        User = apps.get_model('advertisements', 'User')
        user: User = User.objects.all()
        
        context['select_user'] = user
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super(AddNews, self).get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        add_news_form = AddNewsForm(request.POST)
        
        # print(f'{add_news_form.is_valid()=}')
        
        if add_news_form.is_valid():
            NewsItem.objects.create(**add_news_form.cleaned_data)
            
            return HttpResponseRedirect('/news')
        
        context['add_news_form'] = add_news_form
        
        return self.render_to_response(context=context)
