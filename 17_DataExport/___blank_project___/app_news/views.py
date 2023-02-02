# Create your views here.
from django.views import generic

from app_news.models import News


class NewsListView(generic.ListView):
    template_name = 'pages/news/news.html'
    model = News
    context_object_name = 'news_list'
    
    main_header = 'Новости'
    page_title = f'{main_header}'
    
    def get_queryset(self):
        queryset = super(NewsListView, self).get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        return context


class NewsItemDetailView(generic.DetailView):
    template_name = 'pages/news/news_item.html'
    model = News
    context_object_name = 'news_item'
    
    main_header = 'О пользователе'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(NewsItemDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        return context
