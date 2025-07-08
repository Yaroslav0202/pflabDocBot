import os
import io
import tempfile
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches
from pdf2docx import Converter
from config import ROBOTO_FONT, DEFAULT_OUTPUT_FOLDER

class FileProcessor:
    @staticmethod
    def convert_to_pdf(input_path, output_folder):
        """Конвертирует DOCX в PDF с сохранением изображений и форматирования"""
        if input_path.endswith('.pdf'):
            return input_path
            
        try:
            # Создаем временный PDF-файл
            pdf_path = os.path.join(output_folder, "converted.pdf")
            
            # Конвертируем через pdf2docx (сохраняет изображения и стили)
            cv = Converter(input_path)
            cv.convert(pdf_path, start=0, end=None)
            cv.close()
            
            return pdf_path
        except Exception as e:
            raise Exception(f"Ошибка: {str(e)}")

    @staticmethod
    def create_pdfs_for_students(students_list, input_path, output_folder=DEFAULT_OUTPUT_FOLDER):
        """Основная функция для создания PDF с подписями"""
        try:
            # Конвертируем в PDF (если это DOCX)
            if not input_path.endswith('.pdf'):
                input_path = FileProcessor.convert_to_pdf(input_path, output_folder)
            
            if not os.path.exists(input_path):
                yield f"Ошибка: Файл {input_path} не найден"
                return

            os.makedirs(output_folder, exist_ok=True)
            FileProcessor.register_fonts()

            for student in students_list:
                result = FileProcessor.process_single_student(student, input_path, output_folder)
                yield result

        except Exception as e:
            yield f"Ошибка: {str(e)}"
        finally:
            # Удаляем временный файл после конвертации
            if "converted.pdf" in input_path:
                try:
                    os.remove(input_path)
                except:
                    pass

    @staticmethod
    def process_single_student(student, input_pdf_path, output_folder):
        """Добавляет подпись ученика в PDF"""
        # try:
        with open(input_pdf_path, "rb") as pdf_file:
            existing_pdf = PdfReader(pdf_file)
            pdf_width = float(existing_pdf.pages[0].mediabox[2])
            pdf_height = float(existing_pdf.pages[0].mediabox[3])

            # Создаем подпись
            watermark_pdf = FileProcessor.create_watermark(student, pdf_width, pdf_height)

            # Пишем подпись на страницах
            output = PdfWriter()
            for page in existing_pdf.pages:
                page.merge_page(watermark_pdf.pages[0])
                output.add_page(page)

            # Сохраняем PDF
            output_filename = os.path.join(output_folder, f"Работа_{student}.pdf")
            with open(output_filename, "wb") as output_stream:
                output.write(output_stream)

            return output_filename

        # except Exception as e:
        #     return f"Ошибка для ученика {student}: {str(e)}"

    @staticmethod
    def register_fonts():
        """Регистрирует шрифты"""
        try:
            if os.path.exists(ROBOTO_FONT):
                pdfmetrics.registerFont(TTFont("Roboto", ROBOTO_FONT))
            else:
                pdfmetrics.registerFont(TTFont("Helvetica", "Helvetica-Bold"))
        except Exception as e:
            print(f"Ошибка регистрации шрифтов: {e}")

    @staticmethod
    def create_watermark(text, width, height):
        """Создает подпись"""
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        
        # Пытаемся использовать шрифты
        for font in ["Roboto", "Helvetica-Bold", "Helvetica", "Times-Roman"]:
            try:
                can.setFont(font, 15)
                break
            except:
                continue
        
        can.drawString(20, height - 30, text)  # Подпись слева сверху
        can.save()
        
        packet.seek(0)
        return PdfReader(packet)
