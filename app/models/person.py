from app.database import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True, viewonly=True)
    
    def __repr__(self):
        return f'<Person {self.id}: {self.name}>'

    @property
    def has_car(self):
        return len(self.cars) > 0
