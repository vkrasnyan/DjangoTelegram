from django.urls import path
from .views import login_via_telegram, telegram_auth, welcome_view


urlpatterns = [
    path('login/', login_via_telegram, name='login'),
    path('telegram_callback/', telegram_auth, name='telegram_callback'),
    path('welcome/', welcome_view, name='welcome'),
]
