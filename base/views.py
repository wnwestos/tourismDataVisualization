from django.views.generic import View
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from .models import User
from django.utils import timezone
import hashlib
import json
from django.utils.decorators import method_decorator

def login_required(func):
    def wrapper(request, *args, **kwargs):
        # 从request中获取登录时保存的nt_id
        username = request.session.get('username', None)
        if username:
            request.session.set_expiry(9000)
            return func(request, *args, **kwargs)
        else:
            return redirect('/go/login/')
    return wrapper

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        req_type = data['type']
        if req_type == 'reg':
            new_user = User(
                username= username,
                password = hashlib.md5(data['password'].encode('utf-8')).hexdigest(),
                department='development',
                email=username+'@163.com',
                created_at = timezone.now(),
                role='staff'
            )
            try:
                new_user.save()
            except Exception as err:
                return JsonResponse({'code': '-1', 'message': 'Failed to add user.' + str(err)})
            return JsonResponse({'code': '0', 'message': 'New user added!'})
        else:
            user = User.objects.get(pk=username) if User.objects.filter(pk=username).exists() else None
            if user is not None and user.verify_password(password):
                request.session['username'] = username
                request.session.set_expiry(9000)
                return JsonResponse({'code': 0})
            else:
                return JsonResponse({'code': -1,'err':'用户名或密码不匹配！'})

class LogoutManager(View):
    @method_decorator(login_required)
    def get(self, request):
        del request.session['username']
        return redirect('/go/login/')