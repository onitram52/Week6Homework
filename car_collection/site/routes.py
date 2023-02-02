from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from car_collection.forms import CarForm
from car_collection.models import Car, db

site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')
    

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_car = CarForm()
    try:
        if request.method == "POST" and my_car.validate_on_submit():
            name = my_car.name.data
            description = my_car.description.data
            price = my_car.price.data
            color = my_car.color.data
            horsepower = my_car.horsepower.data
            max_speed = my_car.max_speed.data
            dimensions = my_car.dimensions.data
            weight = my_car.weight.data
            cost_of_production = my_car.cost_of_production.data
            make = my_car.make.data
            model = my_car.model.data
            user_token = current_user.token

            car = Car(name, description, price, color, horsepower, max_speed, dimensions, weight, cost_of_production, make, model, user_token)

            db.session.add(car)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Drone not created, please check your form and try again!")

    user_token = current_user.token

    cars = Car.query.filter_by(user_token = user_token)


    return render_template('profile.html', form = my_car, cars = cars)