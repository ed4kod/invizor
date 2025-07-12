#!/usr/bin/env python3
"""
Скрипт для создания тестовых изображений
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_test_image(text, filename, size=(400, 300), bg_color=(52, 152, 219), text_color=(255, 255, 255)):
    """Создает тестовое изображение с текстом"""
    # Создаем изображение
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Добавляем текст
    try:
        # Пытаемся использовать системный шрифт
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Если не найден, используем стандартный
        font = ImageFont.load_default()
    
    # Центрируем текст
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Сохраняем изображение
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    file_path = uploads_dir / filename
    img.save(file_path, "JPEG", quality=85)
    print(f"✅ Создано изображение: {filename}")

def main():
    """Создает тестовые изображения"""
    print("🎨 Создаем тестовые изображения...")
    
    # Создаем папку uploads если её нет
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # Создаем тестовые изображения
    test_images = [
        ("Ноутбук Dell XPS 13", "laptop.jpg", (400, 300), (52, 152, 219)),
        ("Принтер HP LaserJet", "printer.jpg", (400, 300), (231, 76, 60)),
        ("Рабочий стол", "desk.jpg", (400, 300), (46, 204, 113)),
        ("Офисное кресло", "chair.jpg", (400, 300), (155, 89, 182)),
        ("Монитор Samsung", "monitor.jpg", (400, 300), (241, 196, 15)),
    ]
    
    for text, filename, size, color in test_images:
        create_test_image(text, filename, size, color)
    
    print("🎉 Все тестовые изображения созданы!")
    print("📁 Файлы сохранены в папке: uploads/")

if __name__ == "__main__":
    main() 