import telebot
from handlers import register_handlers

import time


API_TOKEN = '8025056970:AAEEPKspp6Wwa8DcipHlKihc-uiF93g7YZI'
bot = telebot.TeleBot(API_TOKEN, parse_mode='Markdown')


def main():
    """Основная функция, регистрирует обработчики и запускает бота."""
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(100)
        main()


if __name__ == '__main__':
    register_handlers(bot)
    main()