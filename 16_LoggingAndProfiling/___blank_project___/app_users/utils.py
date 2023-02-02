from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Sum
from loguru import logger

from app_market.models import Order
from app_users.models import UserStatus


def get_user_orders_data(user: User):
    """
    Вычисление статуса пользователя
    :param user:
    :return:
    """
    orders = Order.objects.filter(user=user, paid_at__isnull=False)
    orders_count = orders.count()
    user_status = 'Деревянный покупатель'
    orders_summ_format = 0
    if orders_count > 0:
    
        orders = Order.objects.annotate(
            total_paid=F('order_item__price') * F('order_item__amount')
        ).filter(user=user, paid_at__isnull=False)
        
        orders_summ: dict = orders.aggregate(Sum('total_paid'))
        orders_summ_format = orders_summ.get('total_paid__sum', 0)
        
        status = UserStatus.objects.filter(expenses_lt__gt=int(orders_summ_format)).order_by('expenses_lt')
        
        user_status = 'Деревянный покупатель'
        if orders_summ:
            user_status = status[0].title
            
        counted_status = status.first()
        current_status = UserStatus.objects.get(id=user.profile.user_status)
        
        if counted_status.id != user.profile.user_status:
            logger.add('logs/statuses.log', level='DEBUG')
            logger.info(f'{user.username} сменил статус: «{current_status.title}» > «{counted_status.title}»')
            user.profile.user_status = counted_status.id
            user.profile.save()
    
    return user_status, orders_count, orders_summ_format
