import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from . models import TelegramProfile
import secrets


logger = logging.getLogger(__name__)
def login_via_telegram(request):
    token = secrets.token_urlsafe(16)
    # Сформировать URL для Telegram-бота
    bot_username = 'myloginetbot'
    telegram_link = f"https://t.me/{bot_username}?start={token}"

    # Сохранить токен
    request.session['auth_token'] = token

    return render(request, 'login.html', {'telegram_link': telegram_link})


def telegram_callback(request):
    telegram_id = request.GET.get('telegram_id')
    telegram_username = request.GET.get('username')
    token = request.GET.get('token')

    try:
        user = User.objects.get(username=telegram_username)
        # Обновляем профиль
        profile = user.telegramprofile
        profile.telegram_id = telegram_id
        profile.telegram_username = telegram_username
        profile.save()
    except User.DoesNotExist:
        user = User.objects.create(username=telegram_username)
        profile = TelegramProfile.objects.create(
            user=user,
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            auth_token=token
        )

    login(request, user)
    return redirect('welcome')


def welcome_view(request):
    username = request.user.username
    return render(request, 'welcome.html', {'username': username})

