import logging
import hashlib
import hmac
import time
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from . models import TelegramProfile
from django.contrib.auth.decorators import login_required


BOT_TOKEN = 'YourBotToken'


def login_via_telegram(request):
    """
    Отображает страницу с Telegram Login Widget.
    """
    return render(request, 'login.html')


@csrf_exempt
def telegram_auth(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        auth_date = int(data['auth_date'])
        hash_value = data['hash']
        check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash'])
        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        calculated_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != hash_value:
            return JsonResponse({'error': 'Invalid hash'}, status=403)
        if time.time() - auth_date > 86400:
            return JsonResponse({'error': 'Auth date expired'}, status=403)

        telegram_id = data['id']
        username = data.get('username', f'user_{telegram_id}')

        user, created = User.objects.get_or_create(username=username)
        TelegramProfile.objects.get_or_create(user=user, telegram_id=telegram_id, telegram_username=username)

        login(request, user)
        return JsonResponse({'status': 'success'})


@login_required
def welcome_view(request):
    """
    Отображает страницу приветствия после успешной авторизации.
    """
    return render(request, 'welcome.html', {'username': request.user.username})

