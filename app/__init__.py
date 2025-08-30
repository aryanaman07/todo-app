from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timezone
from zoneinfo import ZoneInfo

# create database object globally
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['APP_TIMEZONE'] = 'Asia/Kolkata'

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    # import models so user loader can access User
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.about import about_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(about_bp)

    # create DB tables if they don't exist
    with app.app_context():
        db.create_all()

    # Jinja filter to format datetimes in local time
    @app.template_filter('localtime')
    def localtime(dt, fmt='%d %b %Y, %I:%M %p'):
        if not dt:
            return ''
        if dt.tzinfo is None:  
            dt = dt.replace(tzinfo=timezone.utc)
        tz = ZoneInfo(app.config.get('APP_TIMEZONE', 'UTC'))
        return dt.astimezone(tz).strftime(fmt)

    return app
