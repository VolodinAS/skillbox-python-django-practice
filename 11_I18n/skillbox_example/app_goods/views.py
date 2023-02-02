from _csv import reader
from decimal import Decimal
from io import StringIO

from django.http import HttpResponse
from django.shortcuts import render

from app_goods.forms import UploadPriceFileForm
from app_goods.models import Item


def item_list(request, *args, **kwargs):
    items = Item.objects.all()
    return render(request, 'goods/items_list.html', {'items_list': items})


def update_prices(request):
    if request.method == 'POST':
        upload_file_form = UploadPriceFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            price_file = upload_file_form.cleaned_data['file'].read()
            price_str = price_file.decode('utf-8').split('\n')[:-1]
            csv_reader = reader(price_str, delimiter=",", quotechar='"')
            for row in csv_reader:
                Item.objects.filter(code=row[0]).update(price=Decimal(row[1]))
            return HttpResponse(content='Цены были успешно обновлены', status=200)
    else:
        upload_file_form = UploadPriceFileForm()

    context = {
        'form': upload_file_form
    }
    return render(request, 'media/upload_file.html', context=context)
