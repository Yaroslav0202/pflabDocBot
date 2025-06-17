from email import message_from_file

from keyboards import main_keyboard, back_keyboard
from datetime import datetime, timedelta
import telebot
from telebot import types


# def send_pdf_menu(bot, message):
#     """Отправляет меню с доступными олимпиадами пользователю."""
#     bot.delete_message(message.from_user.id, message.message.message_id)
#
#     keyboard.add(telebot.types.InlineKeyboardButton(text=olymp['name'], callback_data=f'olymp_{olymp["id"]}'))
#     bot.send_message(message.from_user.id, "Выберите олимпиаду:", reply_markup=keyboard)
#     bot.send_message(message.from_user.id, "Нет доступных олимпиад.")

def register_handlers(bot: telebot.TeleBot):
    """Регистрирует обработчики команд и сообщений для бота."""

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        bot.send_message(message.chat.id, "Отправьте файл (pdf)")

    @bot.message_handler(content_types=['Document'])
    async def handle_pdf(message):
        if message.document.mime_type == 'application/pdf':
            file_path = f"downloaded_{message.document.file_name}"
            await message.document.download(destination_file=file_path)
            await message.answer(f"PDF-файл сохранён как {file_path}")
        else:
            await message.answer("Пожалуйста, отправьте PDF-файл.")