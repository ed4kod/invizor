#!/usr/bin/env python3
"""
Скрипт для миграции базы данных
"""

from app.database import engine, SessionLocal
from app.models import Base, Asset
from sqlalchemy import text

def migrate_database():
    """Миграция базы данных"""
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли колонка image_url
        result = db.execute(text("PRAGMA table_info(assets)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'image_url' in columns and 'image_filename' not in columns:
            print("🔄 Выполняем миграцию базы данных...")
            
            # Добавляем новую колонку image_filename
            db.execute(text("ALTER TABLE assets ADD COLUMN image_filename TEXT"))
            
            # Копируем данные из image_url в image_filename (если есть)
            db.execute(text("UPDATE assets SET image_filename = image_url WHERE image_url IS NOT NULL"))
            
            # Удаляем старую колонку image_url
            db.execute(text("ALTER TABLE assets DROP COLUMN image_url"))
            
            db.commit()
            print("✅ Миграция завершена успешно!")
            
        elif 'image_filename' in columns:
            print("✅ База данных уже обновлена")
        else:
            print("ℹ️ База данных не требует миграции")
            
    except Exception as e:
        print(f"❌ Ошибка при миграции: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_database() 