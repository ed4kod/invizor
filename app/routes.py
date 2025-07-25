from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User, Bill, Asset
from . import db
import os
import uuid

bp = Blueprint('main', __name__)

def allowed_file(filename):
    """Проверяет, разрешён ли тип файла"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """Сохраняет загруженный файл и возвращает путь"""
    if file and allowed_file(file.filename):
        # Создаём уникальное имя файла
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Создаём папку для загрузок, если её нет
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Сохраняем файл
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Возвращаем относительный путь для сохранения в БД
        return f'uploads/{unique_filename}'
    return None

@bp.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if not user:
            session.pop('user_id', None)
            return redirect(url_for('main.login'))
        bills = Bill.query.filter_by(user_id=user.id).all()
        
        # Загружаем имущество для каждого счета
        for bill in bills:
            bill.assets = Asset.query.filter_by(bill_id=bill.id).all()
        
        return render_template('index.html', user=user, bills=bills)
    return redirect(url_for('main.login'))

@bp.route('/add_bill', methods=['POST'])
def add_bill():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    name = request.form['name']
    description = request.form['description']
    bill = Bill(name=name, description=description, user_id=session['user_id'])
    db.session.add(bill)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует')
            return redirect(url_for('main.register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Войдите.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash('Неверные имя пользователя или пароль')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))

@bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@bp.route('/bill/<int:bill_id>', methods=['GET', 'POST'])
def bill_detail(bill_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    bill = Bill.query.get_or_404(bill_id)
    if bill.user_id != session['user_id']:
        flash('Нет доступа к этому счёту')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        # Добавление имущества
        name = request.form['name']
        inventory_number = request.form['inventory_number']
        registration_date = request.form['registration_date']
        balance_value = request.form['balance_value']
        quantity = request.form['quantity']
        location = request.form['location']
        note = request.form['note']
        status = request.form['status']
        
        asset = Asset(
            name=name,
            inventory_number=inventory_number,
            registration_date=registration_date,
            balance_value=float(balance_value),
            quantity=int(quantity),
            location=location,
            note=note,
            status=status,
            bill_id=bill.id
        )
        db.session.add(asset)
        db.session.commit()
        
        # Обработка загруженных изображений
        files = request.files.getlist('images')
        for file in files:
            if file and file.filename:
                image_path = save_uploaded_file(file)
                if image_path:
                    asset.add_image(image_path)
        
        db.session.commit()
        return redirect(url_for('main.bill_detail', bill_id=bill.id))
    
    assets = Asset.query.filter_by(bill_id=bill.id).all()
    
    # Создаем список URL-ов изображений для каждого имущества
    for asset in assets:
        asset.image_urls = [url_for('static', filename=image) for image in asset.get_images()]
    
    return render_template('bill_detail.html', bill=bill, assets=assets)

@bp.route('/asset/<int:asset_id>/add_images', methods=['POST'])
def add_images_to_asset(asset_id):
    """Добавляет изображения к существующему имуществу"""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    asset = Asset.query.get_or_404(asset_id)
    bill = Bill.query.get(asset.bill_id)
    if bill.user_id != session['user_id']:
        flash('Нет доступа к этому имуществу')
        return redirect(url_for('main.index'))
    
    files = request.files.getlist('images')
    for file in files:
        if file and file.filename:
            image_path = save_uploaded_file(file)
            if image_path:
                if not asset.add_image(image_path):
                    flash('Достигнут лимит в 10 изображений')
                    break
    
    db.session.commit()
    return redirect(url_for('main.asset_detail', asset_id=asset.id))

@bp.route('/asset/<int:asset_id>/remove_image/<int:image_index>', methods=['POST'])
def remove_image_from_asset(asset_id, image_index):
    """Удаляет изображение из имущества"""
    if 'user_id' not in session:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return redirect(url_for('main.login'))
    
    asset = Asset.query.get_or_404(asset_id)
    bill = Bill.query.get(asset.bill_id)
    if bill.user_id != session['user_id']:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        flash('Нет доступа к этому имуществу')
        return redirect(url_for('main.index'))
    
    # Удаляем изображение из БД
    removed_image_path = asset.remove_image(image_index)
    if removed_image_path:
        # Удаляем файл с диска
        try:
            file_path = os.path.join(current_app.root_path, 'static', removed_image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
        
        db.session.commit()
        
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': True, 'message': 'Изображение удалено'})
        flash('Изображение удалено')
    else:
        if request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': False, 'error': 'Ошибка при удалении изображения'})
        flash('Ошибка при удалении изображения')
    
    return redirect(url_for('main.asset_detail', asset_id=asset.id))

@bp.route('/asset/<int:asset_id>')
def asset_detail(asset_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    asset = Asset.query.get_or_404(asset_id)
    bill = Bill.query.get(asset.bill_id)
    if bill.user_id != session['user_id']:
        flash('Нет доступа к этому имуществу')
        return redirect(url_for('main.index'))
    
    # Создаем список URL-ов изображений для JavaScript
    image_urls = [url_for('static', filename=image) for image in asset.get_images()]
    
    return render_template('asset_detail.html', asset=asset, bill=bill, image_urls=image_urls) 