from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired, Length

db = SQLAlchemy()


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    color = StringField(
        'color',
        validators=[DataRequired(), Length(7, 7)]
    )
    cat_or_dog = RadioField(
        'Cat or Dog',
        choices=[('cat', 'Cat'), ('dog', 'Dog')]

    )


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    cat_or_dog = db.Column(db.String)

    def __init__(self, name, color, cat_or_dog):
        super().__init__()
        self.name = name
        self.color = color
        self.cat_or_dog = cat_or_dog