import os
from pdf2docx import Converter
from docx2pdf import convert
from config import TEMP_FOLDER

def convert_to_pdf(input_path, output_folder=TEMP_FOLDER):
    """Конвертирует файл в PDF"""
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}.pdf")
    
    if ext.lower() == '.pdf':
        return input_path
        
    try:
        if ext.lower() in ['.doc', '.docx']:
            convert(input_path, output_path)
        else:
            raise ValueError("Unsupported file format")
            
        return output_path
    except Exception as e:
        raise Exception(f"Conversion error: {str(e)}")

def cleanup_temp_files():
    """Очистка временных файлов"""
    for filename in os.listdir(TEMP_FOLDER):
        file_path = os.path.join(TEMP_FOLDER, filename)
        try:
            os.remove(file_path)
        except:
            pass