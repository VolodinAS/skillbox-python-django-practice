import json
import os.path
from time import time as unix

from django.http import HttpRequest

from app_users.models import Profile


class CreateProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # code
        
        if request.user.is_authenticated:
            profile, created_profile = Profile.objects.get_or_create(
                user=request.user,
                defaults={
                    'user': request.user,
                    # 'city': None,
                    # 'birthday': '2000-01-01',
                    # 'phone': None,
                    # 'avatar_file': None,
                    'balance': 0
                }
            )
        
        response = self.get_response(request)
        
        return response
