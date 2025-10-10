import asyncio
from tasks.celery_conf import celery_app
import telebot
from src.config import settings


@celery_app.task
def newsletter_users(users: list[int], mes: str):
    bot = telebot.TeleBot(settings.BOT_TOKEN)
    for i in users:
        bot.send_message(chat_id=i, text=mes)