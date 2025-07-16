from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    bills = db.relationship('Bill', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>' 

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    assets = db.relationship('Asset', backref='bill', lazy=True)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    inventory_number = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.String(20), nullable=False)
    balance_value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    # фото пока не реализуем 