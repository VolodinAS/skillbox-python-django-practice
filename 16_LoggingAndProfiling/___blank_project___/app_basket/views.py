# Create your views here.
import datetime

from django.db import transaction
from django.db.models import F
from django.db.models import Sum
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from loguru import logger

from app_basket.basket import Cart
from app_market.models import Good
from app_market.models import Order
from app_market.models import OrderItem


class BasketPaidListView(generic.ListView):
    """
    Отображение списка всех заказов
    """
    template_name = 'pages/basket/paid_list.html'
    model = Order
    context_object_name = 'order_list'
    
    page_title = 'Ваши заказы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title

        # prefetch_related('image_good_images'). \
        orders_np = Order.\
            objects.\
            annotate(
                total_paid=Sum(F('order_item__price') * F('order_item__amount'))
            ).\
            filter(
                user=self.request.user,
                paid_at__isnull=True
            )

        # prefetch_related('image_good_images'). \
        orders_p = Order.\
            objects.\
            annotate(
                total_paid=Sum(F('order_item__price') * F('order_item__amount'))
            ).\
            filter(
                user=self.request.user,
                paid_at__isnull=False
            )
        
        # orders_np = Order.objects.filter(user=self.request.user, paid_at__isnull=True)

        context['orders_np'] = orders_np
        context['orders_p'] = orders_p
    
        return context


class BasketPaidDetailView(generic.DetailView):
    """
    Страница оплаты заказа
    """
    template_name = 'pages/basket/paid.html'
    model = Order
    context_object_name = 'order'
    page_title = 'Оплата заказа'
    queryset = Order.objects.all()

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        print(f'{self.kwargs=}')
        
        queryset = super(BasketPaidDetailView, self).get_queryset()
        queryset = queryset.annotate(
            total_paid=Sum(F('order_item__price') * F('order_item__amount'))
        ).filter(id=order_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
    
        return context


class BasketView(generic.TemplateView):
    """
    Корзина
    """
    template_name = 'pages/basket/basket.html'
    page_title = 'Ваша корзина'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Удаление товара из корзины
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        if request.POST:
            if request.POST['good_id']:
                good_id = request.POST['good_id']
                good = Good.objects.get(id=good_id)
                
                cart = Cart(request)
                cart.remove(good)
        
        red = reverse('page_basket')
        return redirect(red)


def confirm_order(request):
    """
    Подтверждение заказа - переводит товары из корзины в заказ
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        all_good = False
        with transaction.atomic():
            new_order = Order.objects.create(
                user=request.user,
                create_at=datetime.datetime.now()
            )
            if new_order.id:
                cart = Cart(request)
                # print(cart)
                data: dict
                for data in cart:
                    quantity = data.get('quantity')
                    price = data.get('price')
                    product: Good = data.get('product')
                    
                    new_order_item = OrderItem.objects.create(
                        order=new_order,
                        good=product,
                        price=price,
                        amount=quantity
                    )

                cart.clear()
                all_good = True
            else:
                return HttpResponse('Проблема с обработкой корзины')
            
        if all_good:
            logger.remove()
            logger.add('logs/basket_to_order.log', level='DEBUG')
            logger.info(f'{request.user.username} подтвердил свой заказ №{new_order.id}')
            red = reverse('page_paid', kwargs={
                'pk': new_order.id
            })
            return redirect(red)
    else:
        return HttpResponse('Вы не авторизованы для покупок')
