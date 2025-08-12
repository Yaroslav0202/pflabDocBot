import os
import subprocess
from pathlib import Path
from config import TEMP_FOLDER

def convert_with_libreoffice(input_file, output_dir):
    """
    Конвертация DOC/DOCX в PDF через LibreOffice.
    """
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", output_dir, input_file
    ], check=True)

def convert_to_pdf(bot, message):
    """
    Конвертирует полученный файл и отправляет PDF.
    """
    user_id = message.from_user.id
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_extension = file_path.split('.')[-1].lower()
    file_name = os.path.splitext(message.document.file_name)[0]

    if file_extension in ("doc", "docx"):
        if file_info.file_size <= 100 * 1024 * 1024:
            temp_dir = Path(TEMP_FOLDER)
            temp_dir.mkdir(parents=True, exist_ok=True)

            input_file = temp_dir / f"{user_id}.{file_extension}"
            output_dir = temp_dir

            bot.download_file(file_path, str(input_file))
            bot.send_message(message.chat.id, "Файл загружен! Конвертирую в PDF...")

            try:
                convert_with_libreoffice(str(input_file), str(output_dir))
                pdf_path = output_dir / f"{user_id}.pdf"
                final_pdf = output_dir / f"{file_name}.pdf"
                pdf_path.rename(final_pdf)

                with open(final_pdf, "rb") as f:
                    bot.send_document(message.chat.id, f)

            except subprocess.CalledProcessError as e:
                bot.send_message(message.chat.id, f"Ошибка при конвертации: {e}")
    else:
        bot.send_message(message.chat.id, "Поддерживаются только файлы .doc и .docx")
