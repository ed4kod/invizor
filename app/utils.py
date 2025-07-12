import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Optional

# Папка для загрузки файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Разрешенные типы файлов
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def is_valid_image_file(filename: str) -> bool:
    """Проверяет, является ли файл допустимым изображением"""
    if not filename:
        return False
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file: UploadFile) -> Optional[str]:
    """Сохраняет загруженный файл и возвращает имя файла"""
    if not file or not is_valid_image_file(file.filename):
        return None
    
    # Генерируем уникальное имя файла
    file_extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        return unique_filename
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return None

def delete_file(filename: str) -> bool:
    """Удаляет файл по имени"""
    if not filename:
        return False
    
    file_path = UPLOAD_DIR / filename
    try:
        if file_path.exists():
            file_path.unlink()
            return True
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")
    return False

def get_file_url(filename: str) -> str:
    """Возвращает URL для доступа к файлу"""
    if not filename:
        return ""
    return f"/uploads/{filename}" 