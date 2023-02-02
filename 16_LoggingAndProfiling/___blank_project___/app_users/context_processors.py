from django.contrib.auth.models import User
# from app_news.models import NewsItem
from django.http import HttpRequest
from django.urls import reverse

from app_basket.basket import Cart
from app_market.models import Order


def add_variable_to_context(request: HttpRequest):
    """
    Добавление дополнительных переменных во все страницы
    :param request:
    :return:
    """
    variables = dict()
    cart = Cart(request)
    if request.user.is_authenticated:
        variables['balance'] = request.user.profile.balance
        url = reverse('page_replenish_balance')
        variables[
            'balance_format'] = f'<b>Текущий баланс:</b> ${"{:.2f}".format(request.user.profile.balance)}. <a href="{url}"><b>Пополнить</b></a>'
        
        orders_total = Order.objects.filter(user=request.user)
        orders_not_paid = Order.objects.filter(paid_at__isnull=True)
        orders_paid = Order.objects.filter(paid_at__isnull=False)

        variables['orders_total'] = orders_total.count()
        variables['orders_not_paid'] = orders_not_paid.count()
        variables['orders_paid'] = orders_paid.count()

        # variables['orders_t'] = orders_total
        # variables['orders_np'] = orders_not_paid
        # variables['orders_p'] = orders_paid
    
    variables['cart'] = cart
    
    variables['cart_length_format'] = f"Товаров в Вашей корзине: {len(cart)} на общую сумму: ${cart.get_total_price()}"
    return variables
