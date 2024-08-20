from flask import Blueprint, request, jsonify

from app.database import db
from app.models import Person


person_bp = Blueprint('person', __name__, url_prefix='/persons')


@person_bp.route('/', methods=['GET'])
def get_persons():
    persons = Person.query.all()
    return jsonify([person.to_dict() for person in persons]), 200


@person_bp.route('/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get_or_404(id)
    return jsonify(person.to_dict()), 200


@person_bp.route('/', methods=['POST'])
def create_person():
    data = request.json
    person = Person(name=data['name'])
    db.session.add(person)
    db.session.commit()
    return jsonify(person.to_dict()), 201


@person_bp.route('/<int:id>', methods=['PUT'])
def update_person(id):
    person = Person.query.get_or_404(id)
    data = request.json
    person.name = data['name']
    db.session.commit()
    return jsonify(person.to_dict()), 200


@person_bp.route('/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return '', 204