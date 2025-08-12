from telebot import types
import os
from config import STATES, SUPPORTED_FORMATS
from keyboards import get_main_keyboard
from operations import FileProcessor

class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.user_states = {}  # Хранит состояние каждого пользователя
        self.file_processor = FileProcessor(bot)  # Создаём FileProcessor с bot

    def handle_start(self, message):
        """Приветственное сообщение."""
        self.bot.reply_to(
            message,
            "Бот для создания PDF с подписями\n"
            "Выберите действие ниже",
            reply_markup=get_main_keyboard()
        )

    def handle_help(self, message):
        """Показывает справку."""
        help_text = (
            "<b>Как использовать бота:</b>\n"
            "1. Нажмите <b>\"Создать PDF с подписями\"</b>\n"
            "2. Отправьте файл (PDF, DOC или DOCX)\n"
            "3. Получите готовый PDF"
        )
        self.bot.send_message(message.chat.id, help_text, parse_mode="HTML")

    def handle_create_pdf(self, message):
        """Устанавливает состояние пользователя для загрузки файла."""
        chat_id = message.chat.id
        self.user_states[chat_id] = STATES["waiting_for_file"]
        self.bot.send_message(chat_id, "Отправьте мне файл (PDF, DOC или DOCX)")

    def handle_document(self, message):
        """Обрабатывает присланный файл."""
        chat_id = message.chat.id
        state = self.user_states.get(chat_id)

        if state == STATES["waiting_for_file"]:
            self.file_processor.process_file
