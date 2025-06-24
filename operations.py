import os
import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from config import ROBOTO_FONT, DEFAULT_OUTPUT_FOLDER

def create_pdfs_for_students(students_list, input_pdf_path, output_folder=DEFAULT_OUTPUT_FOLDER):
    os.makedirs(output_folder, exist_ok=True)
    
    # Регистрация шрифтов
    register_fonts()

    for student in students_list:
        try:
            existing_pdf = PdfReader(open(input_pdf_path, "rb"))
            pdf_width = float(existing_pdf.pages[0].mediabox[2])
            pdf_height = float(existing_pdf.pages[0].mediabox[3])

            watermark_pdf = create_watermark_pdf(
                text=student,
                width=pdf_width,
                height=pdf_height
            )

            output = PdfWriter()
            for page in existing_pdf.pages:
                watermark_page = watermark_pdf.pages[0]
                page.merge_page(watermark_page)
                output.add_page(page)

            output_filename = os.path.join(output_folder, f"Работа_{student}.pdf")
            with open(output_filename, "wb") as output_stream:
                output.write(output_stream)
            
            yield output_filename
        except Exception as e:
            yield f"Ошибка для ученика {student}: {str(e)}"

def register_fonts():
    try:
        # Пытаемся зарегистрировать Roboto
        if os.path.exists(ROBOTO_FONT):
            pdfmetrics.registerFont(TTFont("Roboto", ROBOTO_FONT))
        else:
            # Если Roboto не найден, используем стандартные шрифты ReportLab
            pdfmetrics.registerFont(TTFont("Helvetica", "Helvetica"))
            pdfmetrics.registerFont(TTFont("Times-Roman", "Times-Roman"))
    except Exception as e:
        print(f"Ошибка регистрации шрифтов: {e}")

def create_watermark_pdf(text, width, height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    # Устанавливаем шрифт (пробуем доступные варианты)
    try:
        can.setFont("Roboto", 15)
    except:
        try:
            can.setFont("Helvetica", 15)
        except:
            can.setFont("Times-Roman", 15)
    
    # Подпись в нижнем левом углу
    can.drawString(20, 20, text)
    can.save()
    
    packet.seek(0)
    return PdfReader(packet)