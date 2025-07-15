import os
import subprocess
import tempfile
from pathlib import Path
from config import TEMP_FOLDER

def convert_to_pdf(input_path, output_folder=TEMP_FOLDER):
    try:
        input_path = Path(input_path)
        output_path = Path(output_folder) / f"{input_path.stem}.pdf"
        
        if input_path.suffix.lower() == '.pdf':
            return str(input_path)
            
        if input_path.suffix.lower() not in ['.doc', '.docx']:
            raise ValueError("Unsupported file format")

        # Создаем временный файл для безопасной конвертации
        with tempfile.NamedTemporaryFile(suffix='.pdf', dir=output_folder) as tmp:
            temp_pdf = Path(tmp.name)
            
            # Конвертируем через unoconv
            result = subprocess.run([
                'unoconv',
                '-f', 'pdf',
                '-o', str(temp_pdf),
                str(input_path)
            ], stderr=subprocess.PIPE)
            
            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8')
                raise RuntimeError(f"unoconv failed: {error_msg}")
            
            # Проверяем что файл создан и не пустой
            if not temp_pdf.exists() or temp_pdf.stat().st_size == 0:
                raise RuntimeError("Conversion failed - empty output file")
            
            # Переносим в итоговое расположение
            temp_pdf.rename(output_path)
            
        return str(output_path)
    except Exception as e:
        raise RuntimeError(f"Conversion error: {str(e)}")

def cleanup_temp_files():
    """Очистка временных файлов"""
    for item in Path(TEMP_FOLDER).glob('*'):
        try:
            if item.is_file():
                item.unlink()
        except Exception:
            pass
