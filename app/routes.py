from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Bill, Asset
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if not user:
            session.pop('user_id', None)
            return redirect(url_for('main.login'))
        bills = Bill.query.filter_by(user_id=user.id).all()
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
        return redirect(url_for('main.bill_detail', bill_id=bill.id))
    assets = Asset.query.filter_by(bill_id=bill.id).all()
    return render_template('bill_detail.html', bill=bill, assets=assets)

@bp.route('/asset/<int:asset_id>')
def asset_detail(asset_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    asset = Asset.query.get_or_404(asset_id)
    bill = Bill.query.get(asset.bill_id)
    if bill.user_id != session['user_id']:
        flash('Нет доступа к этому имуществу')
        return redirect(url_for('main.index'))
    return render_template('asset_detail.html', asset=asset, bill=bill) 