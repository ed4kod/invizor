from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine, Base
from app.routers import auth, accounts, assets

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invizor", description="Система управления имуществом")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Настройка Jinja2 шаблонов
templates = Jinja2Templates(directory="templates")

# Подключение роутеров
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])

@app.get("/")
async def root(request: Request):
    """Главная страница - редирект на логин"""
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 