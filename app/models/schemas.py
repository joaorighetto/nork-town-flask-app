from marshmallow import Schema, fields, validates, post_load, ValidationError
from app.models import Person
from app.database import db


class CarSchema(Schema):
    id = fields.Int(dump_only=True)
    model = fields.Str(required=True)
    color = fields.Str(required=True)
    owner_id = fields.Int(required=True)

    @validates('owner_id')
    def validate_owner_car_limit(self, owner_id):
        user = Person.query.get(owner_id)
        if user and len(user.cars) >= 3:
            raise ValidationError("A user can't own more than 3 cars.")
        
    