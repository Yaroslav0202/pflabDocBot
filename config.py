import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DEFAULT_INPUT_PDF = os.path.join(BASE_DIR, "default.pdf")
DEFAULT_OUTPUT_FOLDER = os.path.join(BASE_DIR, "output_pdfs")
FONTS_FOLDER = os.path.join(BASE_DIR, "fonts")
ROBOTO_FONT = os.path.join(FONTS_FOLDER, "Roboto-Regular.ttf")

os.makedirs(DEFAULT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)

STATES = {
    "WAITING_FOR_PDF": 1,
    "WAITING_FOR_STUDENTS": 2
}