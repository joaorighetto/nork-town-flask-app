from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from app.admin import CarAdminView, PersonAdminView, CustomAdminIndexView
from app.commands import register_commands
from app.database import db
from app.models import Car, Person, User
from app.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    admin = Admin(app, name='nork-town', index_view=CustomAdminIndexView())
    admin.add_view(CarAdminView(Car, db.session))
    admin.add_view(PersonAdminView(Person, db.session))

    
    with app.app_context():
        db.create_all()
        
    init_routes(app)
    register_commands(app)

    return app