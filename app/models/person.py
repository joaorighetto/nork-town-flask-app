from app.database import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True, viewonly=True)
    
    def __repr__(self):
        return f'<Person {self.id}: {self.name}>'
        
    def to_dict(self):
        if self.has_car:
            return {
                'id': self.id,
                'name': self.name,
                'cars': [car.to_dict() for car in self.cars]
            }
        else:
            return {
                'id': self.id,
                'name': self.name
            }

    @property
    def has_car(self):
        return len(self.cars) > 0
