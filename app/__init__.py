from flask import Flask
from flask_admin import Admin

from app.admin.admin import CarAdminView, PersonAdminView
from app.database import db
from app.models import Car, Person


def create_app():
    app = Flask(__name__)
    
    app.config.from_object('instance.config.Config')
    
    admin = Admin(app, name='nork-town')
    admin.add_view(CarAdminView(Car, db.session))
    admin.add_view(PersonAdminView(Person, db.session))

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app