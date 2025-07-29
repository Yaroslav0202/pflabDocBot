from telebot import TeleBot
import os
import subprocess
import tempfile
from keyboards import get_main_keyboard
from pathlib import Path
from config import TEMP_FOLDER
from docx2pdf import convert
from main import bot

def convert_to_pdf(message):
    user_id = message.from_user.id

    if message.document:

        file_id = message.document.file_id
        file_name = message.document.file_name.rsplit('.', 1)[0]
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Получаем расширение файла
        file_extension = file_path.split('.')[-1]

        # Проверяем, что расширение файла соответствует допустимым значениям
        if file_extension.lower() == 'docx':
            # Получаем информацию о размере файла
            file_size = file_info.file_size
            # Проверяем размер файла (до 100 МБ)
            if file_size <= 100 * 1024 * 1024:
                # Сохраняем файл на сервере
                dir = 'Source\\'
                bot.download_file(file_path, (dir + f'{user_id}.{file_extension}'))
                bot.send_message(message.chat.id,
                'Файл успешно загружен! Процесс займет несколько секунд')

                # Конвертируем DOCX в PDF
                docx_file = dir + f'{user_id}.{file_extension}'
                pdf_file = dir + f'{file_name}.pdf'
                convert(docx_file, pdf_file)

                # Отправка файла пользователю
                with open(pdf_file, 'rb') as file:
                    bot.send_document(message.chat.id, file)

def cleanup_temp_files():
    """Очистка временных файлов"""
    for item in Path(TEMP_FOLDER).glob('*'):
        try:
            if item.is_file():
                item.unlink()
        except Exception:
            pass
