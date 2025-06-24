from telebot import TeleBot
from config import BASE_DIR
from handlers import Handlers
from keyboards import get_main_keyboard
import os

# Инициализвция бота
bot = TeleBot("8025056970:AAEEPKspp6Wwa8DcipHlKihc-uiF93g7YZI")
handlers = Handlers(bot)

# Команда start
@bot.message_handler(commands=['start'])
def start(message):
    handlers.handle_start(message)

# Команда help
@bot.message_handler(commands=['help'])
def help(message):
    handlers.handle_help(message)

# Вывод кнопки помощи на клавиатуре снизу
@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_button(message):
    handlers.handle_help(message)

# Вывод кнопки создания PDF на клавиатуре снизу
@bot.message_handler(func=lambda message: message.text == "Создать PDF с подписями")
def create_pdf(message):
    handlers.handle_create_pdf(message)

# Функция запуска бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
