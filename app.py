import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from enum import Enum


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)


# MODELS
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)
    
    def add_car(self, car):
        if len(self.cars) >= 3:
            raise ValueError("An owner can have only up to 3 cars")
        self.cars.append(car)


class CarColor(Enum):
    YELLOW = "yellow"
    BLUE = "blue"
    GRAY = "gray"
    
    
class CarModel(Enum):
    HATCH = "hatch"
    SEDAN = "sedan"
    CONVERTIBLE = "convertible"
    
    
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Enum(CarModel), nullable=False)
    color = db.Column(db.Enum(CarColor), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


@app.route('/')
def home():
    return "Hello, World!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)