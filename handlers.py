from telebot import types
import os
from config import STATES, DEFAULT_INPUT_PDF
from keyboards import get_main_keyboard, get_cancel_keyboard
from operations import create_pdfs_for_students

class Handlers:
    def __init__(self, bot):
        self.bot = bot
        self.user_states = {}

    def handle_start(self, message):
        self.bot.reply_to(
            message,
            "Это бот для создания PDF с подписями учеников",
            reply_markup=get_main_keyboard()
        )

    def handle_help(self, message):
        help_text = """
Как использовать бота:
1. Нажмите кнопку 'Создать PDF с подписями'
2. Отправьте PDF файл для подписи (или используйте стандартный)
3. Отправьте список учеников (каждый с новой строки)
4. Получите готовые PDF файлы

Команды:
/start - начать работу
/help - помощь
"""
        self.bot.send_message(message.chat.id, help_text)

    def handle_create_pdf(self, message):
        self.user_states[message.chat.id] = {"state": STATES["WAITING_FOR_PDF"]}
        msg = self.bot.send_message(
            message.chat.id,
            "Отправьте PDF файл (default /skip):",
            reply_markup=get_cancel_keyboard()
        )
        self.bot.register_next_step_handler(msg, self.process_pdf_step)

    def process_pdf_step(self, message):
        chat_id = message.chat.id
        
        if message.text == "Отмена":
            self.bot.send_message(chat_id, "Действие отменено", reply_markup=get_main_keyboard())
            return
        
        if message.text == "/skip":
            self.user_states[chat_id] = {
                "state": STATES["WAITING_FOR_STUDENTS"],
                "input_pdf": DEFAULT_INPUT_PDF
            }
            msg = self.bot.send_message(
                chat_id,
                "Отправьте список учеников (каждый с новой строки):",
                reply_markup=get_cancel_keyboard()
            )
            self.bot.register_next_step_handler(msg, self.process_students_step)
            return
        
        if not message.document or not message.document.file_name.endswith('.pdf'):
            msg = self.bot.send_message(chat_id, "Отправьте PDF файл (default /skip)")
            self.bot.register_next_step_handler(msg, self.process_pdf_step)
            return
        
        try:
            file_info = self.bot.get_file(message.document.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            temp_pdf_path = f"temp_{chat_id}.pdf"
            with open(temp_pdf_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            self.user_states[chat_id] = {
                "state": STATES["WAITING_FOR_STUDENTS"],
                "input_pdf": temp_pdf_path
            }
            self.bot.send_message(
                chat_id,
                "PDF получен. Отправьте список учеников (каждый с новой строки):",
                reply_markup=get_cancel_keyboard()
            )
        except Exception as e:
            self.bot.reply_to(message, f"Ошибка: {e}")
            self.bot.send_message(chat_id, "Попробуйте снова", reply_markup=get_main_keyboard())

    def process_students_step(self, message):
        chat_id = message.chat.id
        
        if message.text == "Отмена":
            self.cleanup_user_data(chat_id)
            self.bot.send_message(chat_id, "Действие отменено", reply_markup=get_main_keyboard())
            return
        
        students = [s.strip() for s in message.text.split('\n') if s.strip()]
        
        if not students:
            msg = self.bot.send_message(chat_id, "Список пуст. Отправьте список учеников:")
            self.bot.register_next_step_handler(msg, self.process_students_step)
            return
        
        user_data = self.user_states.get(chat_id, {})
        input_pdf = user_data.get("input_pdf", DEFAULT_INPUT_PDF)
        
        # self.bot.send_message(chat_id, f"Обрабатываю {len(students)} учеников...")
        
        try:
            for result in create_pdfs_for_students(students, input_pdf):
                if result.endswith('.pdf'):
                    with open(result, 'rb') as f:
                        self.bot.send_document(chat_id, f)
                    os.remove(result)
                else:
                    self.bot.send_message(chat_id, result)
            
            self.bot.send_message(chat_id, "Готово!", reply_markup=get_main_keyboard())
        except Exception as e:
            self.bot.send_message(chat_id, f"Ошибка: {e}")
        finally:
            self.cleanup_user_data(chat_id)

    def cleanup_user_data(self, chat_id):
        if chat_id in self.user_states:
            user_data = self.user_states[chat_id]
            if "input_pdf" in user_data and user_data["input_pdf"] != DEFAULT_INPUT_PDF:
                if os.path.exists(user_data["input_pdf"]):
                    os.remove(user_data["input_pdf"])
            del self.user_states[chat_id]
