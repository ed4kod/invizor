from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .auth import SECRET_KEY, ALGORITHM

async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
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

def require_auth(func):
    """Декоратор для проверки аутентификации"""
    async def wrapper(request: Request, *args, **kwargs):
        db = next(get_db())
        user = await get_current_user_from_cookie(request, db)
        
        if not user:
            return RedirectResponse(url="/auth/login", status_code=303)
        
        # Добавляем пользователя в request
        request.state.user = user
        return await func(request, *args, **kwargs)
    
    return wrapper 