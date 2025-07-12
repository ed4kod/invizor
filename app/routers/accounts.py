from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt

from ..database import get_db
from ..models import User, Account
from ..auth import SECRET_KEY, ALGORITHM
from ..schemas import AccountCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_current_user_from_cookie(request: Request, db: Session):
    """Получение текущего пользователя из cookie"""
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        return None
    
    try:
        # Убираем "Bearer " префикс если есть
        if access_token.startswith("Bearer "):
            access_token = access_token[7:]
        
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.username == username).first()
    return user

@router.get("/", response_class=HTMLResponse)
async def accounts_list(request: Request, db: Session = Depends(get_db)):
    """Список счетов пользователя"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    accounts = db.query(Account).filter(Account.owner_id == current_user.id).all()
    return templates.TemplateResponse(
        "accounts.html", 
        {"request": request, "accounts": accounts, "user": current_user}
    )

@router.post("/")
async def create_account(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    """Создание нового счета"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    db_account = Account(
        name=name,
        description=description,
        owner_id=current_user.id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return RedirectResponse(url="/accounts", status_code=303)

@router.get("/{account_id}", response_class=HTMLResponse)
async def account_detail(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Детальная информация о счете"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.owner_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Счет не найден")
    
    return templates.TemplateResponse(
        "account_detail.html", 
        {"request": request, "account": account, "user": current_user}
    ) 