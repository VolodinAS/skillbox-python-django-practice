from django.shortcuts import render


def advertisement_list(request, *args, **kwargs):
    advertisements = [
        'Мастер на час',
        'Выведение из запоя',
        'Услуги экскаватора-погрузчика, гидромолота, ямобура'
    ]
    advertisements_1 = [
        'Мастер на час',
        'Выведение из запоя',
        'Услуги экскаватора-погрузчика, гидромолота, ямобура'
    ]
    return render(request, 'advertisements_bak/advertisement_list.html', {'advertisements_bak': advertisements,
                                                                      'advertisements_1': advertisements_1})

