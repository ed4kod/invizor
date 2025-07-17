from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask import g, session

# Создание экземпляра базы данных
# (экземпляр будет инициализирован позже)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'  # Для сессий
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes
    app.register_blueprint(routes.bp)

    @app.before_request
    def load_logged_in_user():
        g.user = None
        user_id = session.get('user_id')
        if user_id is not None:
            from app.models import User
            g.user = User.query.get(user_id)

    return app 