from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token
from ..auth import authenticate_user, create_access_token, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Страница входа"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Обработка входа пользователя"""
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Неверное имя пользователя или пароль"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/accounts", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя"""
    # Проверяем, существует ли пользователь
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Пользователь с таким именем или email уже существует"}
        )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Перенаправляем на страницу входа
    return RedirectResponse(url="/auth/login", status_code=303)

@router.get("/logout")
async def logout():
    """Выход из системы"""
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response 