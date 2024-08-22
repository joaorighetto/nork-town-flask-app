from enum import Enum
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

from app.database import db


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
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete="CASCADE"), nullable=False)

    @validates('owner_id')
    def validate_owner_car_limit(self, key, owner_id):
        owner_cars_count = db.session.query(Car).filter_by(owner_id=owner_id).count()
        if owner_cars_count >= 3:
            raise IntegrityError('Owner cannot have more than 3 cars.', params=None, orig=None)
        return owner_id