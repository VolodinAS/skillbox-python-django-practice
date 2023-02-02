import json
import os.path
import random
from json import JSONDecodeError
from random import randint

from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from loguru import logger

from app_basket.basket import Cart
from app_market.forms import CartAddProductForm
from app_market.models import *
from app_users.utils import get_user_orders_data
from utils.get_file_extension_by_url import get_file_extension_by_url
from utils.pretty import pretty


class MarketListView(generic.ListView):
    """
    Главная страница - список товаров
    """
    template_name = 'pages/market/market.html'
    page_title = 'Добро пожаловать в «МаркетПлейс»'
    model = Good
    # queryset = Good.objects.all()
    context_object_name = 'goods_list'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(MarketListView, self).get_context_data(**kwargs)
        
        context['page_title'] = self.page_title
        
        return context


class MarketDetailView(generic.DetailView):
    """
    Детальное описание товара
    """
    template_name = 'pages/market/detail.html'
    page_title = 'Подробнее о товаре'
    model = Good
    # queryset = Good.objects.all()
    context_object_name = 'good_item'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        GET
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(MarketDetailView, self).get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['form'] = cart_product_form
        context['page_title'] = self.page_title
        
        return context
    
    # @require_POST
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Добавление товара в корзину
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        context = super(MarketDetailView, self).get_context_data(**kwargs)
        
        good_item: Good = self.object
        
        cart = Cart(request)
        
        print(cart.get_total_price())
        
        product = get_object_or_404(Good, id=good_item.id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['quantity'].isdigit():
                cart.add(product=product,
                         quantity=int(cd['quantity']),
                         update_quantity=cd['update'])
                context['msg'] = 'Товар добавлен в корзину'
                context['msg_theme'] = 'success'
            else:
                context['msg'] = 'Количество должно быть целым числом!'
                context['msg_theme'] = 'warning'
        
        cart_product_form = CartAddProductForm()
        context['form'] = cart_product_form
        context['page_title'] = self.page_title
        
        print(context)
        
        red = reverse('page_market_item', kwargs={
            'pk': good_item.pk
        })
        return redirect(red + '?status=1')
        # return self.render_to_response(context=context)


class MarketImportFromJson(generic.TemplateView):
    """
    Импорт данных из json-fake
    """
    template_name = 'pages/market/import.html'
    page_title = 'Импорт данных из JSON'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        # json_file = os.path.join('app_market', 'temp', 'goods_json.json')
        json_file = 'blank.json'
        
        if os.path.exists(json_file):
            data: None
            with open(json_file, 'r') as f:
                try:
                    data: list = json.load(f)
                except JSONDecodeError:
                    logger.error(f'{json_file} is invalid')
            
            good: dict
            shop_list = list(Shop.objects.all())
            for good in data:
                pretty(good)
                good_id = good.get('id')
                if good_id:
                    random.shuffle(shop_list)
                    # print(shop_list[0])
                    good_title = good.get('title', f'title_of_{good_id}')
                    good_desc = good.get('description', f'description_of_{good_id}')
                    good_price = good.get('price', randint(100, 500))
                    good_remain = randint(50, 1000)
                    good_face_image = good.get('thumbnail', '')
                    good_images = good.get('images', [])
                    good_shop = shop_list[0]
                    
                    image_ext = get_file_extension_by_url(good_face_image)
                    new_image_name = f'good_face_{good_id}.{image_ext}'
                    
                    new_good: Good = Good(
                        title=good_title,
                        description=good_desc,
                        shop=good_shop,
                        price=good_price,
                        remains=good_remain
                    )
                    
                    new_good.get_image_from_url(good_face_image, new_image_name)
                    new_good.save()
                    
                    if new_good.id:
                        logger.success(f'Товар {good_title} добавлен в {shop_list[0]}')
                        
                        if len(good_images) > 0:
                            index = 0
                            for image in good_images:
                                image_ext = get_file_extension_by_url(image)
                                new_image_name = f'good_{good_id}_{index}.{image_ext}'
                                good_image = GoodImages(
                                    good=new_good
                                )
                                good_image.get_image_from_url(
                                    url=image,
                                    new_name=new_image_name
                                )
                                good_image.save()
                                
                                if good_image.id:
                                    index += 1
                                    logger.success(f'Фотография {new_image_name} товара {good_title} добавлены')
                    
                    else:
                        logger.error(f'Ошибка при добавлении товара {good} в базу!')
                
                # print()
                # break
        
        else:
            logger.error(f'{json_file} doesnt exists')
        
        return context


class MarketPaidSuccess(generic.TemplateView):
    """
    Оплата заказа
    """
    template_name = 'pages/market/success.html'
    
    main_header = 'Оплата товара'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['msg'] = 'Заказ успешно оплачен!'
        context['msg_theme'] = 'success'
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Подтверждение оплаты заказа
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        
        order_id = request.POST.get('order_id', 0)
        order = Order.objects.filter(id=order_id)
        if order.exists():
            
            with transaction.atomic():
                order = order.first()
                # order.paid_at = datetime.datetime.now()
                order.paid_at = timezone.now()
                user = request.user
                expenses = float(order.total_paid())
                user.profile.balance -= expenses
                user.profile.save()
                order.save()
                
                good: Good
                for order_item in order.order_item.all():
                    good: Good = order_item.good
                    good.remains -= float(order_item.amount)
                    good.save()
                
                logger.remove()
                logger.add('logs/paid_order.log', level='DEBUG')
                logger.info(f'{request.user.username} оплатил заказ №{order.id}')
                
                logger.remove()
                logger.add('logs/balance.log', level='DEBUG')
                logger.info(f'У {request.user.username} списано ${expenses} за заказ №{order.id}')

                user_status, orders_count, orders_summ_format = get_user_orders_data(self.request.user)
                
                red = reverse('page_paid_success')
                return redirect(red)
        
        else:
            context['msg'] = 'Заказ не найден!'
            context['msg_theme'] = 'warning'
        
        context['page_title'] = self.page_title
        return self.render_to_response(context=context)
