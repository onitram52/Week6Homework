from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import db, Car, car_schema, cars_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):
    nickname = request.json['nickname']
    description = request.json['description']
    price = request.json['price']
    color = request.json['color']
    horsepower = request.json['horsepower']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    make = request.json['make']
    model = request.json['model']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(nickname, description, price, color, horsepower, max_speed, dimensions, weight, cost_of_production, make, model, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(our_user):
    owner = our_user.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)

    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401

@api.route('/cars/<id>', methods = ['PUT', 'POST'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)
    car.nickname = request.json['nickname']
    car.description = request.json['description']
    car.price = request.json['price']
    car.color = request.json['color']
    car.horsepower = request.json['horsepower']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_production = request.json['cost_of_production']
    car.make = request.json['make']
    car.model = request.json['model']
    car.user_token = our_user.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_cars(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()


    response = car_schema.dump(car)
    return jsonify(response)