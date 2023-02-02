from random import randint

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import TemplateView
from loguru import logger

from .forms import EditProfileForm
from .forms import RegForm
from .forms import ReplenishBalanceForm
from .forms import UserLoginForm
from .models import Profile
from .utils import get_user_orders_data


class UserProfile(TemplateView):
    template_name = 'profile/index.html'
    
    main_header = 'Профиль{username}'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        
        data = {}
        if self.request.user.is_authenticated:
            data['first_name'] = self.request.user.first_name
            data['last_name'] = self.request.user.last_name
            if hasattr(self.request.user, 'profile'):
                data['city'] = self.request.user.profile.city
                data['birthday'] = self.request.user.profile.birthday
                data['phone'] = self.request.user.profile.phone
                data['avatar'] = self.request.user.profile.avatar_file
        
        # print(f'{data=}')
        
        form = EditProfileForm(data)
        
        username = f' {self.request.user.username}'
        self.page_title = self.page_title.format(username=username)
        
        context = super().get_context_data(**kwargs)
        
        user_status, orders_count, orders_summ_format = get_user_orders_data(self.request.user)
        
        context['user_status'] = user_status
        context['orders_count'] = orders_count
        context['orders_summ'] = orders_summ_format
        context['page_title'] = self.page_title
        context['form'] = form
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = f' {self.request.user.username}'
        self.page_title = self.page_title.format(username=username)
        
        context['page_title'] = self.page_title
        
        form = EditProfileForm(request.POST, request.FILES)
        
        context['form'] = form
        
        if request.user.is_authenticated:
            
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                birthday = form.cleaned_data.get('birthday')
                city = form.cleaned_data.get('city')
                phone = form.cleaned_data.get('phone')
                
                user_update: User = User.objects.get(id=request.user.id)
                user_update.first_name = first_name
                user_update.last_name = last_name
                user_update.last_name = last_name
                user_update.save()
                
                try:
                    profile_update: Profile = Profile.objects.get(user_id=request.user.id)
                except ObjectDoesNotExist:
                    profile_update = Profile.objects.create(
                        user=request.user,
                        city=city,
                        birthday=birthday,
                        phone=phone
                    )
                
                profile_update.birthday = birthday
                profile_update.city = city
                profile_update.phone = phone
                if request.FILES:
                    file: InMemoryUploadedFile = request.FILES['avatar_file']
                    file_name = file.name
                    file_ext = file_name[-3::]
                    request.FILES['avatar_file'].name = f'avatar_{request.user.id}.{file_ext}'
                    profile_update.avatar_file.delete()
                    profile_update.avatar_file = request.FILES['avatar_file']
                
                profile_update.save()
                
                # print(f"{request.FILES['avatar_file'].name=}")
                
                context['msg'] = 'Профиль успешно обновлён'
                context['msg_theme'] = 'success'
        
        else:
            context['msg'] = 'Неавторизованным пользователям нет доступа к редактированию профиля'
            context['msg_theme'] = 'warning'
        
        user_status, orders_count, orders_summ_format = get_user_orders_data(self.request.user)
        
        context['user_status'] = user_status
        context['orders_count'] = orders_count
        context['orders_summ'] = orders_summ_format
        
        return self.render_to_response(context=context)


class LoginAuthView(LoginView):
    template_name = 'pages/auth/auth.html'
    authentication_form = UserLoginForm
    
    main_header = 'Авторизация'
    page_title = f'{main_header}'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        logger.add('logs/auth.log', level='DEBUG')
        logger.info(f'Пользователь {username} успешно авторизовался')
        print('123123')
        return super(LoginAuthView, self).form_valid(form)


class LogoutAuthView(LogoutView):
    template_name = 'auth_template/logout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        logout_page_data = self.request.META['HTTP_REFERER']
        host_data: str = self.request.META['HTTP_HOST']
        
        logout_page_arr: list = logout_page_data.split(host_data + '/')
        
        if len(logout_page_arr) >= 2:
            logout_page = logout_page_arr[1]
        else:
            logout_page = '/'
        
        context['logout_page'] = logout_page
        
        return context


class RegView(TemplateView):
    template_name = 'pages/auth/reg.html'
    
    main_header = 'Регистрация'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        """
        GET
        :param kwargs:
        :return:
        """
        
        num1 = randint(1, 10)
        num2 = randint(1, 10)
        summa = num1 + num2
        
        self.request.session['summa'] = summa
        
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        context['num1'] = num1
        context['num2'] = num2
        # context['summa'] = summa
        
        user_reg_form = RegForm()
        
        context['form'] = user_reg_form
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        form = RegForm(request.POST)
        
        if form.is_valid():
            captcha: str = form.cleaned_data.get('captcha')
            
            captcha_session = request.session.get('summa')
            
            if not captcha.isdigit():
                form.add_error('captcha', 'Решение должно быть числом!')
            else:
                captcha: int = int(captcha)
                if captcha == captcha_session:
                    
                    new_user = form.save()
                    
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    birthday = form.cleaned_data.get('birthday')
                    phone = form.cleaned_data.get('phone')
                    city = form.cleaned_data.get('city')
                    
                    # print(f'{username=}')
                    # print(f'{password=}')
                    # print(f'{birthday=}')
                    # print(f'{phone=}')
                    # print(f'{city=}')
                    
                    if new_user.id:
                        new_profile = Profile.objects.create(
                            user=new_user,
                            city=city,
                            birthday=birthday,
                            phone=phone
                        )
                        
                        if new_profile.id:
                            
                            unverified_group = Group.objects.get(name='Зарегистрированные пользователи')
                            unverified_group.user_set.add(new_user)
                            
                            user = authenticate(username=username, password=password)
                            login(request, user)
                            return redirect('/')
                        else:
                            form.add_error(None, 'Проблема с добавлением профиля в БД')
                    else:
                        form.add_error(None, 'Проблема с добавлением пользователя в БД')
                
                else:
                    form.add_error('captcha', 'Пример решен неверно!')
        
        context['form'] = form
        
        return self.render_to_response(context=context)


class ReplenishBalance(generic.TemplateView):
    template_name = 'pages/profile/replenish.html'
    
    main_header = 'Пополнить баланс'
    page_title = f'{main_header}'
    
    def get_context_data(self, **kwargs):
        context = super(ReplenishBalance, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        replenish_form = ReplenishBalanceForm()
        
        context['form'] = replenish_form
        
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        
        replenish_form = ReplenishBalanceForm(request.POST)
        
        if replenish_form.is_valid():
            money = replenish_form.cleaned_data.get('money', 0)
            if money > 0:
                user = User.objects.get(pk=request.user.id)
                print(f'{user.profile.balance=}')
                user.profile.balance += money
                print(f'{user.profile.balance=}')
                user.profile.save()
                replenish_form = ReplenishBalanceForm()
                
                logger.remove()
                logger.add('logs/replenish.log', level='DEBUG')
                logger.info(f'{request.user.username} пополнил баланс на ${money}')
                
                context['msg'] = f'Баланс успешно пополнен на <b>${money}</b>'
                context['msg_theme'] = 'success'
            else:
                replenish_form.add_error('money', 'Введите число больше 0')
        
        context['form'] = replenish_form
        
        return self.render_to_response(context=context)
