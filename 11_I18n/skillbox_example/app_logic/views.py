from django.shortcuts import render

def welcome(request, *args, **kwargs):
    return render(request, 'welcome.html')
