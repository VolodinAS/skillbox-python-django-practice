from django.views import generic

from app_houses.models import *


class HouseListView(generic.ListView):
    template_name = 'pages/houses/houses.html'
    model = House
    context_object_name = 'house_list'
    
    main_header = 'Недвижимость'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class HouseDetailView(generic.DetailView):
    template_name = 'pages/houses/detail.html'
    model = House
    context_object_name = 'house_item'
    
    main_header = 'О недвижимости'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(HouseDetailView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        return context
