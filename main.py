from telebot import TeleBot
from handlers import Handlers
import os
from secrets import TOKEN

# Инициализация бота
bot = TeleBot(TOKEN)
handlers = Handlers(bot)

"""Регистрация обработчиков"""
@bot.message_handler(commands=['start', 'help'])
def handle_commands(message):
    if message.text == '/start':
        handlers.handle_start(message)
    else:
        handlers.handle_help(message)

@bot.message_handler(func=lambda m: m.text in ["Создать PDF с подписями", "Помощь"])
def handle_buttons(message):
    if message.text == "Создать PDF с подписями":
        handlers.handle_create_pdf(message)
    else:
        handlers.handle_help(message)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    if handlers.user_states.get(chat_id, {}).get("state") == 1:  # WAITING_FOR_FILE
        handlers.process_file_step(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    if handlers.user_states.get(chat_id, {}).get("state") == 2:  # WAITING_FOR_STUDENTS
        handlers.process_students_step(message)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
