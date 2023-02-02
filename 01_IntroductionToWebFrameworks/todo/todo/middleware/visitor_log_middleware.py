import json
import os.path
from time import time as unix

from django.http import HttpRequest


class VisitorLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest):
        # code
        
        ip = request.META['REMOTE_ADDR']
        method = request.META['REQUEST_METHOD']
        path = request.META['PATH_INFO']
        
        log_file = os.getcwd()
        log_file = os.path.join(log_file, 'logs', 'visits.json')
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf') as json_file:
                json_file.write(json.dumps([]))
        
        with open(log_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        
        visit_data = {
            'ip': ip,
            'time': int(unix()),
            'method': method,
            'path': path
        }
        json_data.append(visit_data)
        
        with open(log_file, 'w', encoding='utf-8') as json_f:
            json_f.write(json.dumps(json_data))
        
        response = self.get_response(request)
        
        return response
