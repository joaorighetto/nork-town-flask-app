import pytest
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Car, CarModel, CarColor, Person


def test_owner_car_limit(app_context):
    person = Person(name="John Doe")
    db.session.add(person)
    db.session.commit()
    
    person = Person.query.get(person.id)
    
    car1 = Car(model=CarModel.HATCH, color=CarColor.YELLOW, owner_id=person.id)
    car2 = Car(model=CarModel.SEDAN, color=CarColor.BLUE, owner_id=person.id)
    car3 = Car(model=CarModel.CONVERTIBLE, color=CarColor.RED, owner_id=person.id)
    
    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.commit()    
    
    with pytest.raises(IntegrityError):
        car4 = Car(model=CarModel.HATCH, color=CarColor.BLUE, owner_id=person.id)
        db.session.add(car4)
        db.session.commit()
        

def test_car_cant_exist_without_owner(app_context):
    car = Car(model=CarModel.HATCH, color=CarColor.YELLOW)
    
    with pytest.raises(IntegrityError):
        db.session.add(car)
        db.session.commit()
        

def test_delete_person_and_owned_cars(app_context):
    person = Person(name="John Doe")
    db.session.add(person)
    db.session.commit()
    
    person = Person.query.get(person.id)
    
    car1 = Car(model=CarModel.HATCH, color=CarColor.YELLOW, owner_id=person.id)
    car2 = Car(model=CarModel.SEDAN, color=CarColor.BLUE, owner_id=person.id)
    car3 = Car(model=CarModel.CONVERTIBLE, color=CarColor.RED, owner_id=person.id)
    
    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.commit()    
    
    db.session.delete(person)
    db.session.commit()
    
    assert Car.query.filter_by(owner_id=person.id).count() == 0