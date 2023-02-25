from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_character.forms import CharacterForm
from marvel_character.models import Character, db

site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')
    

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_character = CharacterForm()
    try:
        if request.method == "POST" and my_character.validate_on_submit():
            name = my_character.name.data
            description = my_character.description.data
            comics_appeared_in = my_character.comics_appeared_in.data
            super_power = my_character.super_power.data
            date_created = my_character.date_created.data
            user_token = current_user.token

            character = Character(name, description, comics_appeared_in, super_power, date_created, user_token)

            db.session.add(character)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Drone not created, please check your form and try again!")

    user_token = current_user.token

    characters = Character.query.filter_by(user_token = user_token)


    return render_template('profile.html', form = my_character, characters = characters)