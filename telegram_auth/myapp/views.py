import logging
import hashlib
import hmac
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import TelegramProfile


BOT_TOKEN = 'YourBotToken'


def login_via_telegram(request):
    return render(request, 'login.html')


def telegram_auth(request):
    auth_data = request.POST.dict()

    # Проверяем подпись данных
    if not validate_telegram_auth(auth_data):
        return HttpResponseBadRequest("Неверная подпись данных")

    telegram_id = auth_data.get('id')
    username = auth_data.get('username')

    # Ищем существующего пользователя
    try:
        profile = TelegramProfile.objects.get(telegram_id=telegram_id)
        user = profile.user
    except TelegramProfile.DoesNotExist:
        user = User.objects.create(username=username or f"tg_user_{telegram_id}")
        TelegramProfile.objects.create(
            user=user,
            telegram_id=telegram_id,
            telegram_username=username
        )

    # Логиним пользователя
    login(request, user)
    next_url = request.GET.get('next', 'welcome')
    return redirect(next_url)


def validate_telegram_auth(auth_data):
    """
    Проверка подписи данных от Telegram.
    """
    check_hash = auth_data.pop('hash', None)
    auth_data_sorted = sorted(auth_data.items())
    data_check_string = "\n".join([f"{k}={v}" for k, v in auth_data_sorted])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Проверка подписи и времени
    auth_date = int(auth_data.get('auth_date', 0))
    if abs(time.time() - auth_date) > 86400:  # 24 часа
        return False

    return check_hash == calculated_hash

@login_required
def welcome_view(request):
    return render(request, 'welcome.html', {'username': request.user.username})

