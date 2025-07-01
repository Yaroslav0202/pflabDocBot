import os
import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document  # Для работы с Word
from config import ROBOTO_FONT, DEFAULT_OUTPUT_FOLDER, SUPPORTED_FORMATS

class FileProcessor:
    @staticmethod
    def convert_to_pdf(input_path, output_folder):
        # Конвертирует DOC/DOCX в PDF (если требуется)
        if input_path.endswith('.pdf'):
            return input_path  # Если PDF, возвращаем исходный файл
            
        try:
            doc = Document(input_path)  # Читаем Word-документ
            pdf_path = os.path.join(output_folder, "converted.pdf")
            
            # Создаем PDF из текста Word
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            
            FileProcessor.register_fonts()  # Регистрируем шрифты
            
            # Переносим текст из Word в PDF
            y = 700  # Начальная позиция текста
            for para in doc.paragraphs:
                if y < 50:  # Если текст не помещается, создаем новую страницу
                    can.showPage()
                    y = 700
                can.setFont("Roboto", 12)
                can.drawString(50, y, para.text)
                y -= 20
            
            can.save()
            packet.seek(0)
            
            # Сохраняем PDF
            with open(pdf_path, "wb") as f:
                f.write(packet.getvalue())
                
            return pdf_path
        except Exception as e:
            raise Exception(f"Ошибка конвертации: {str(e)}")

    @staticmethod
    def create_pdfs_for_students(students_list, input_path, output_folder=DEFAULT_OUTPUT_FOLDER):
        """Создает PDF с подписями учеников."""
        try:
            # Конвертируем в PDF, если это Word
            if not input_path.endswith('.pdf'):
                input_path = FileProcessor.convert_to_pdf(input_path, output_folder)
            
            if not os.path.exists(input_path):
                yield f"Файл {input_path} не найден"
                return

            os.makedirs(output_folder, exist_ok=True)
            FileProcessor.register_fonts()

            # Добавляем подписи для каждого ученика
            for student in students_list:
                result = FileProcessor.process_single_student(student, input_path, output_folder)
                yield result

        except Exception as e:
            yield {str(e)}
        finally:
            # Удаляем временный PDF после конвертации
            if input_path.endswith('converted.pdf'):
                try:
                    os.remove(input_path)
                except:
                    pass

    @staticmethod
    def process_single_student(student, input_pdf_path, output_folder):
        # Добавляет подпись ученика в PDF
        try:
            with open(input_pdf_path, "rb") as pdf_file:
                existing_pdf = PdfReader(pdf_file)
                pdf_width = float(existing_pdf.pages[0].mediabox[2])
                pdf_height = float(existing_pdf.pages[0].mediabox[3])

                # Создаем водяной знак с именем ученика
                watermark_pdf = FileProcessor.create_watermark(student, pdf_width, pdf_height)

                # Накладываем подпись на страницы
                output = PdfWriter()
                for page in existing_pdf.pages:
                    page.merge_page(watermark_pdf.pages[0])
                    output.add_page(page)

                # Сохраняем PDF
                output_filename = os.path.join(output_folder, f"Работа_{student}.pdf")
                with open(output_filename, "wb") as output_stream:
                    output.write(output_stream)

                return output_filename

        except Exception as e:
            return f"Ошибка для ученика {student}: {str(e)}"

    @staticmethod
    def register_fonts():
        """Регистрирует шрифты (Roboto или стандартные)."""
        try:
            if os.path.exists(ROBOTO_FONT):
                pdfmetrics.registerFont(TTFont("Roboto", ROBOTO_FONT))
            else:
                pdfmetrics.registerFont(TTFont("Helvetica", "Helvetica-Bold"))
        except Exception as e:
            print(f"Ошибка регистрации шрифтов: {e}")

    @staticmethod
    def create_watermark(text, width, height):
        """Создает водяной знак с текстом."""
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        
        # Пытаемся использовать доступные шрифты
        for font in ["Roboto", "Helvetica-Bold", "Helvetica", "Times-Roman"]:
            try:
                can.setFont(font, 15)
                break
            except:
                continue
        
        can.drawString(20, 20, text)  # Подпись внизу страницы
        can.save()
        
        packet.seek(0)
        return PdfReader(packet)