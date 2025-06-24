import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Пути к файлам
DEFAULT_INPUT_PDF = os.path.join(BASE_DIR, "default.pdf")
DEFAULT_OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_pdfs")
FONTS_FOLDER = os.path.join(BASE_DIR, "fonts")
ROBOTO_FONT = os.path.join(FONTS_FOLDER, "Roboto-Regular.ttf")

# Проверка и создание необходимых папок
os.makedirs(DEFAULT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)

# Состояния бота
STATES = {
    "WAITING_FOR_PDF": 1,
    "WAITING_FOR_STUDENTS": 2
}