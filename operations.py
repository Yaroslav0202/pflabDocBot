import os
from converters import convert_to_pdf
from config import SUPPORTED_FORMATS

class FileProcessor:
    def __init__(self, bot):
        self.bot = bot

    def process_file(self, message):
        file_extension = message.document.file_name.rsplit('.', 1)[-1].lower()
        if file_extension in SUPPORTED_FORMATS:
            convert_to_pdf(self.bot, message)  # передаём bot сюда
        else:
            self.bot.send_message(
                message.chat.id,
                f"Формат .{file_extension} не поддерживается. "
                f"Доступные форматы: {', '.join(SUPPORTED_FORMATS)}"
            )
