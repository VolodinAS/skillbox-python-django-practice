from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import RegForm
from .forms import UserLoginForm
from .models import Profile


class LoginAuthView(LoginView):
    template_name = 'page_login/index.html'
    authentication_form = UserLoginForm
    
    main_header = 'Авторизация'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        # return self.render_to_response(context=context)
        return context


class LogoutAuthView(LogoutView):
    # next_page = '/auth/login'
    template_name = 'auth_template/logout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        logout_page_data = self.request.META['HTTP_REFERER']
        host_data: str = self.request.META['HTTP_HOST']
        # print(host_data)
        # print(logout_page_data)
        
        logout_page_arr: list = logout_page_data.split(host_data + '/')
        # print(f'{logout_page_arr=}')
        
        if len(logout_page_arr) >= 2:
            logout_page = logout_page_arr[1]
        else:
            logout_page = '/'
        # print(f'{logout_page=}')
        context['logout_page'] = logout_page
        # print(self.request.META)
        
        return context


class RegView(TemplateView):
    template_name = 'page_reg/index.html'
    
    main_header = 'Регистрация'
    page_header = f'{main_header} | Django | Skillbox'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        
        context = super().get_context_data(**kwargs)
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        user_reg_form = RegForm()
        
        context['form'] = user_reg_form
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_header'] = self.page_header
        context['page_title'] = self.page_title
        
        form = RegForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            birthday = form.cleaned_data.get('birthday')
            city = form.cleaned_data.get('city')
            
            Profile.objects.create(
                user=user,
                city=city,
                birthday=birthday
            )
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        
        context['form'] = form
        
        return self.render_to_response(context=context)
