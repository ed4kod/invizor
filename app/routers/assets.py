from fastapi import APIRouter, Request, HTTPException, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import JWTError, jwt

from ..database import get_db
from ..models import User, Account, Asset
from ..auth import SECRET_KEY, ALGORITHM
from ..schemas import AssetCreate
from ..utils import save_uploaded_file, delete_file, get_file_url

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

@router.get("/account/{account_id}", response_class=HTMLResponse)
async def assets_list(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Список имущества в счете"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    # Проверяем, что счет принадлежит пользователю
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.owner_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Счет не найден")
    
    assets = db.query(Asset).filter(Asset.account_id == account_id).all()
    
    return templates.TemplateResponse(
        "assets.html", 
        {"request": request, "assets": assets, "account": account, "user": current_user}
    )

@router.post("/account/{account_id}")
async def create_asset(
    request: Request,
    account_id: int,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form("active"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Создание нового имущества"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    # Проверяем, что счет принадлежит пользователю
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.owner_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Счет не найден")
    
    # Сохраняем изображение, если оно загружено
    image_filename = None
    if image:
        image_filename = save_uploaded_file(image)
    
    db_asset = Asset(
        name=name,
        description=description,
        status=status,
        image_filename=image_filename,
        account_id=account_id
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    return RedirectResponse(url=f"/assets/account/{account_id}", status_code=303)

@router.get("/{asset_id}", response_class=HTMLResponse)
async def asset_detail(
    request: Request,
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Детальная информация об имуществе"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    asset = db.query(Asset).join(Account).filter(
        Asset.id == asset_id,
        Account.owner_id == current_user.id
    ).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Имущество не найдено")
    
    return templates.TemplateResponse(
        "asset_detail.html", 
        {"request": request, "asset": asset, "user": current_user}
    )

@router.post("/{asset_id}/update")
async def update_asset(
    request: Request,
    asset_id: int,
    name: str = Form(...),
    description: str = Form(""),
    status: str = Form("active"),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Обновление имущества"""
    current_user = get_current_user_from_cookie(request, db)
    
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=303)
    
    asset = db.query(Asset).join(Account).filter(
        Asset.id == asset_id,
        Account.owner_id == current_user.id
    ).first()
    
    if not asset:
        raise HTTPException(status_code=404, detail="Имущество не найдено")
    
    # Если загружено новое изображение, удаляем старое и сохраняем новое
    if image:
        if asset.image_filename is not None:
            delete_file(str(asset.image_filename))
        new_filename = save_uploaded_file(image)
        asset.image_filename = str(new_filename) if new_filename else None  # type: ignore
    asset.name = str(name)  # type: ignore
    asset.description = str(description)  # type: ignore
    asset.status = str(status)  # type: ignore
    
    db.commit()
    db.refresh(asset)
    
    return RedirectResponse(url=f"/assets/{asset_id}", status_code=303) 