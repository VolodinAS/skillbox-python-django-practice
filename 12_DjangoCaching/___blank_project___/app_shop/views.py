# Create your views here.
from django.views import generic
from django.utils.translation import gettext_lazy as _

from app_shop.models import Shop


class ShopIndexListView(generic.ListView):
    template_name = 'pages/shop/shop_list.html'
    model = Shop
    context_object_name = 'shop_list'
    
    page_title = _('Список магазинов')  #
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ShopIndexListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        return context
