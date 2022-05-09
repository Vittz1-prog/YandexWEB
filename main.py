import os

import sqlite3
from flask import Flask, render_template, request, session, make_response, jsonify, redirect
from flask_login import login_user, current_user, LoginManager, login_required, logout_user

from PIL import Image

from data.recipes import Recipe
from data import db_session
from recipe_add_form import RecipeForm
from data.users import User
from profile_form import ProfileForm
from register_form import RegisterForm
from login_form import LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/steak.sqlite")
    app.run(port=8080, host='127.1.1.1', debug=True)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/", methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        pass
    return render_template("main.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            email=form.email.data,
            hashed_password=form.password.data,
            image_profile="static/img/data/default_avatar.png",
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
        )

        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect("/login")
    return render_template('register.html', title='Register Form', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.id == current_user.id).first()
            user.email = form.email.data
            user.login = form.login.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            session.commit()
            return redirect('/profile')
        if request.method == 'GET':
            session = db_session.create_session()
            user = session.query(User).filter(User.id == current_user.id).first()
            form.email.data = user.email
            form.login.data = user.login
            form.surname.data = user.surname
            form.name.data = user.name
            form.age.data = user.age
            return render_template("profile.html", form=form)
        elif request.method == 'POST':
            try:
                session = db_session.create_session()
                user = session.query(User).filter(User.id == current_user.id).first()
                f = request.files['file']

                f.save(os.path.join(f"static/img/users", f'avatar_{user.id}.png'))
                f = Image.open(f"static/img/users/avatar_{user.id}.png")
                f = f.resize((90, 90))
                f.save(os.path.join(f"static/img/users", f'avatar_{user.id}.png'))

                user.image_profile = f"static/img/users/avatar_{user.id}.png"
                session.commit()
            except Exception:
                pass
            return render_template("profile.html", title='Profile', form=form)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        try:
            recipes = session.query(Recipe).filter(Recipe.user_id == user.id).all()

            recipe = Recipe(
                name=form.name.data,
                text=form.text.data,
                image="static/img/data/default_recipe.png",
                rate=0,
                num=recipes[-1].num + 1,
                user_id=current_user.id,
            )
        except Exception:
            recipe = Recipe(
                name=form.name.data,
                text=form.text.data,
                image="static/img/data/default_recipe.png",
                rate=0,
                num=1,
                user_id=current_user.id,
            )
        session.add(recipe)
        session.commit()
        return redirect("/")
    return render_template('add_recipe.html', title='Recipe Form', form=form)


@app.route('/change_recipes', methods=['GET', 'POST'])
def change_recipes():
    if request.method == 'GET':
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        recipes = session.query(Recipe).filter(Recipe.user_id == user.id).all()

        images = []
        for i in range(len(recipes)):
            images.append(recipes[i].image)
        return render_template("change_recipes.html", images=images)


@app.route('/change_recipe', methods=['GET', 'POST'])
def change_recipe():
    form = RecipeForm()
    if current_user.is_authenticated:
        session = db_session.create_session()
        recipe = session.query(Recipe).filter(Recipe.user_id == current_user.id).all()

        form.name.data = recipe.name
        form.text.data = recipe.text

        if form.validate_on_submit():
            recipe.name = form.name.data
            recipe.text = form.text.data
        if request.method == 'GET':
            return render_template("change_recipe.html", title='Recipe', form=form, recipe=recipe)
        elif request.method == 'POST':
            try:
                f = request.files['file']

                f.save(os.path.join(f"static/img/recipes", f'recipe_{recipe.id}.png'))
                f = Image.open(f"static/img/recipes/recipe_{recipe.id}.png")
                f = f.resize((90, 90))
                f.save(os.path.join(f"static/img/recipes", f'recipe_{recipe.id}.png'))

                recipe.image = f"static/img/recipes/recipe_{recipe.id}.png"
                session.commit()
            except Exception:
                pass
            return render_template("change_recipe.html", title='Recipe', form=form, recipe=recipe)


if __name__ == '__main__':
    main()
