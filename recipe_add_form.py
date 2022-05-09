from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    name = StringField('Имя рецепта', validators=[DataRequired()])
    text = StringField('Текст', validators=[DataRequired()])
    submit = SubmitField('Добавить')