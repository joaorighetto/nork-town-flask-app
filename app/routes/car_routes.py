from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Car, CarModel, CarColor

car_bp = Blueprint('car', __name__, url_prefix='/cars')

@car_bp.route('/', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([car.to_dict() for car in cars]), 200

@car_bp.route('/<int:id>', methods=['GET'])
def get_car(id):
    car = Car.query.get_or_404(id)
    return jsonify(car.to_dict()), 200

@car_bp.route('/', methods=['POST'])
def create_car():
    data = request.json
    car = Car(model=CarModel[data['model']], color=CarColor[data['color']], owner_id=data['owner_id'])
    db.session.add(car)
    db.session.commit()
    return jsonify(car.to_dict()), 201

@car_bp.route('/<int:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.json
    car.model = CarModel[data['model']]
    car.color = CarColor[data['color']]
    car.owner_id = data['owner_id']
    db.session.commit()
    return jsonify(car.to_dict()), 200

@car_bp.route('/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return '', 204