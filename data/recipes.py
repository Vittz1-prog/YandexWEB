import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Recipe(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    num = sqlalchemy.Column(sqlalchemy.Integer)
    text = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    rate = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, name, image, num, text, rate, user_id):
        self.name = name
        self.image = image
        self.num = num
        self.text = text
        self.rate = rate
        self.user_id = user_id

    def change_name(self, new_name):
        self.name = new_name

    def change_image(self, new_image):
        self.image = new_image

    def change_num(self, new_num):
        self.num = new_num

    def change_text(self, new_text):
        self.text = new_text

    def change_rate(self, new_rate):
        self.rate = new_rate

    def change_user_id(self, new_user_id):
        self.user_id = new_user_id

    def check_user_id(self, new_user_id):
        return new_user_id == self.user_id

    def check_rate(self, new_rate):
        return new_rate == self.rate

    def check_text(self, new_text):
        return new_text == self.text

    def check_num(self, new_num):
        return new_num == self.num

    def check_image(self, new_image):
        return new_image == self.image

    def check_name(self, new_name):
        return new_name == self.name
