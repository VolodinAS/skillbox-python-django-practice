from django.http import HttpRequest
from django.views import generic
from django.views.generic import TemplateView

from .models_dir import Advertisement
from .models_dir import Category
from .models_dir import Region


class Index(TemplateView):
    """
    Индекс-страница
    """
    template_name = 'page_index/index.html'
    
    page_header = 'Добро пожаловать! | Django | Skillbox'
    page_title = 'Добро пожаловать!'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        
        category_list = Category.objects.all()
        region_list = Region.objects.all()
        
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        context['category_list'] = category_list
        context['region_list'] = region_list
        
        return context
    
    def post(self, request: HttpRequest, **kwargs):
        """
        POST
        :param request:
        :param kwargs:
        :return:
        """
        
        category_list = Category.objects.all()
        region_list = Region.objects.all()
        
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        context['category_list'] = category_list
        context['region_list'] = region_list
        
        context['form_data'] = request.POST
        
        context['result'] = f'Кажется, я что-то нашел...'
        
        return self.render_to_response(context)


# class Advertisements(TemplateView):
#     template_name = 'page_advertisements/index.html'
#
#     page_header = 'Список объявлений | Django | Skillbox'
#     page_title = 'Список объявлений'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_header'] = self.page_header
#         context['page_title'] = self.page_title
#
#         return context
#
#     def post(self, request: HttpRequest, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_header'] = self.page_header
#         context['page_title'] = self.page_title
#
#         post_count = request.session.get('post_count', 0)
#         post_count += 1
#         request.session['post_count'] = post_count
#
#         context['result'] = f'Объявление успешно добавлено (это уже {post_count}-й запрос)'
#
#         return self.render_to_response(context)


class Contacts(TemplateView):
    """
    Страница контактов
    """
    template_name = 'page_contacts/index.html'
    
    page_header = 'Контакты | Django | Skillbox'
    page_title = 'Наши контакты'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        context['address'] = '445044, Россия, г. Тольятти, Южное шоссе, 89'
        context['phone'] = '8 (8482) 72-54-48'
        context['email'] = 'alex_vovkin@mail.ru'
        
        return context


class About(TemplateView):
    """
    О компании
    """
    template_name = 'page_about/index.html'
    
    page_header = 'О компании | Django | Skillbox'
    page_title = 'О компании'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        context['title'] = 'VolodinAS'
        context['description'] = 'Нам почти 30 лет!'
        
        return context


class AdvertisementList(generic.ListView):
    model = Advertisement
    template_name = 'page_advertisements/index.html'
    context_object_name = 'advertisements'
    
    main_header = 'Список объявлений'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdvertisementList, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context


class AdvertisementDetails(generic.DetailView):
    model = Advertisement
    template_name = 'page_advertisements/details.html'
    context_object_name = 'advertisement'
    
    main_header = 'Детализация объявления'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(AdvertisementDetails, self).get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        return context
