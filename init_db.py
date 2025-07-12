#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных с тестовыми данными
"""

from app.database import engine, SessionLocal
from app.models import Base, User, Account, Asset
from app.auth import get_password_hash

def init_db():
    """Инициализация базы данных"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже пользователи
        existing_user = db.query(User).first()
        if existing_user:
            print("База данных уже содержит данные. Пропускаем инициализацию.")
            return
        
        # Создаем тестового пользователя
        test_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Администратор Системы",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Создаем тестовые счета
        account1 = Account(
            name="Офисное оборудование",
            description="Компьютеры, принтеры и другая офисная техника",
            owner_id=test_user.id
        )
        account2 = Account(
            name="Мебель",
            description="Столы, стулья, шкафы",
            owner_id=test_user.id
        )
        
        db.add(account1)
        db.add(account2)
        db.commit()
        db.refresh(account1)
        db.refresh(account2)
        
        # Создаем тестовое имущество
        assets = [
            Asset(
                name="Ноутбук Dell XPS 13",
                description="Мощный ноутбук для разработки",
                status="active",
                image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
                account_id=account1.id
            ),
            Asset(
                name="Принтер HP LaserJet",
                description="Лазерный принтер для печати документов",
                status="active",
                image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
                account_id=account1.id
            ),
            Asset(
                name="Рабочий стол",
                description="Деревянный стол для работы",
                status="active",
                image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400",
                account_id=account2.id
            ),
            Asset(
                name="Офисное кресло",
                description="Эргономичное кресло с подлокотниками",
                status="active",
                image_url="https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400",
                account_id=account2.id
            ),
            Asset(
                name="Монитор Samsung 24\"",
                description="Монитор с высоким разрешением",
                status="damaged",
                image_url="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400",
                account_id=account1.id
            )
        ]
        
        for asset in assets:
            db.add(asset)
        
        db.commit()
        
        print("✅ База данных успешно инициализирована!")
        print(f"👤 Создан пользователь: {test_user.username} (пароль: admin123)")
        print(f"📋 Создано счетов: 2")
        print(f"🏷️ Создано имущества: {len(assets)}")
        print("\n🔗 Для входа используйте:")
        print("   Логин: admin")
        print("   Пароль: admin123")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 