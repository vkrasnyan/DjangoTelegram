import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TOKEN = 'YourBotToken'
DJANGO_SERVER_URL = 'http://127.0.0.1:8000/telegram_callback'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.args[0] if context.args else None
    if token:
        telegram_id = update.effective_user.id
        telegram_username = update.effective_user.username
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DJANGO_SERVER_URL}?token={token}&telegram_id={telegram_id}&username={telegram_username}"
            )
        await update.message.reply_text("Авторизация успешна! Можете вернуться на сайт.")
    else:
        await update.message.reply_text("Некорректная команда.")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
