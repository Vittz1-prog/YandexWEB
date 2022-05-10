import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    image_profile = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.Text, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __init__(self, name, surname, image_profile, login, age, email, hashed_password):
        self.name = name
        self.surname = surname
        self.image_profile = image_profile
        self.login = login
        self.age = age
        self.email = email
        self.hashed_password = hashed_password

    def change_name(self, new_name):
        self.name = new_name

    def change_surname(self, new_surname):
        self.surname = new_surname

    def change_image_profile(self, new_image_profile):
        self.image_profile = new_image_profile

    def change_login(self, new_login):
        self.login = new_login

    def change_age(self, new_age):
        self.age = new_age

    def change_email(self, new_email):
        self.email = new_email

    def check_email(self, new_email):
        return new_email == self.email

    def check_age(self, new_age):
        return new_age == self.age

    def check_login(self, new_login):
        return new_login == self.login

    def check_image_profile(self, new_image_profile):
        return new_image_profile == self.image_profile

    def check_surname(self, new_surname):
        return new_surname == self.surname

    def check_name(self, new_name):
        return new_name == self.name
