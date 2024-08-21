from enum import Enum
from sqlalchemy.exc import IntegrityError

from app.database import db


class CarColor(Enum):
    YELLOW = "yellow"
    BLUE = "blue"
    RED = "red"  
    
class CarModel(Enum):
    HATCH = "hatch"
    SEDAN = "sedan"
    CONVERTIBLE = "convertible"
    
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Enum(CarModel), nullable=False)
    color = db.Column(db.Enum(CarColor), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete="CASCADE"), nullable=False)

