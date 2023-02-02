from datetime import date
from datetime import timedelta

from django.http import HttpRequest
from django.views import generic

from app_market.models import Order
from app_reports.forms import ReportForm
from utils.sort_dict_by_key import sort_dict_by_two_keys


class ReportView(generic.TemplateView):
    """
    Страница отображения отчёта
    """
    template_name = 'pages/report/report.html'
    page_title = 'Отчёт по продажам'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        report_form = ReportForm()
        
        context['form'] = report_form
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Вывод отчёта с учетом дат
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO ПЕРЕРАБОТАТЬ ЧЕРЕЗ ANNOTATE()
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        report_form = ReportForm(request.POST)
        
        if report_form.is_valid():
            
            orders = Order.objects.filter(paid_at__isnull=False).order_by('-paid_at')
            
            date_from: date = report_form.cleaned_data.get('date_from')
            date_to: date = report_form.cleaned_data.get('date_to')
            
            # print(f'{type(date_from)=}')
            
            if date_from is not None:
                print(f'{date_from=}')
                orders = orders.filter(paid_at__gte=date_from)
            
            if date_to is not None:
                date_to = date_to + timedelta(seconds=86399)  # нам нужно время дд.мм.гггг 23:59:59
                orders = orders.filter(paid_at__lte=date_to)
            
            # orders = orders.annotate(
            #     total_paid=Sum(F('order_item__price') * F('order_item__amount'))
            # ).order_by('total_paid')
            
            # print(f'{orders=}')
            
            sells_good: dict = dict()
            for order in orders:
                for order_item in order.order_item.all():
                    total_summa = order_item.get_total_price()
                    good = order_item.good
                    if good.id not in sells_good:
                        sells_good[good.id] = dict()
                        sells_good[good.id]['amount'] = order_item.amount
                        sells_good[good.id]['total_summa'] = total_summa
                        sells_good[good.id]['good'] = good
                    else:
                        sells_good[good.id]['amount'] += order_item.amount
                        sells_good[good.id]['total_summa'] += total_summa

            sells_good_list: list[dict] = list()
            for good_id, data in sells_good.items():
                sells_good_list.append(data)
            
            # print(sells_good_list)
            
            # print('<DEFAULT LIST>')
            # print(sells_good_list)
            # print('</DEFAULT LIST>')
            # sells_good_list_sorted_1 = sort_dict_by_key(sells_good_list, 'amount')
            # sells_good_list_sorted_2 = sort_dict_by_two_keys(sells_good_list, itemgetter('amount', 'total_summa'))
            sells_good_list_sorted_2 = sort_dict_by_two_keys(sells_good_list, 'amount', 'total_summa')
            
            # print('<SORT_1 LIST>')
            # print(sells_good_list_sorted_1)
            # print('</SORT_1 LIST>')
            #
            # print('<SORT_2 LIST>')
            # print(sells_good_list_sorted_2)
            # print('</SORT_2 LIST>')
            
            context['goods_list'] = sells_good_list_sorted_2
        
        context['form'] = report_form
        
        return self.render_to_response(context=context)
