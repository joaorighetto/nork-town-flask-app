from flask import Flask
from app.database import db
from app.routes.person_routes import person_bp
from app.routes.car_routes import car_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('instance.config.Config')
    app.register_blueprint(person_bp)
    app.register_blueprint(car_bp)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app