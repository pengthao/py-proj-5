from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddRating(FlaskForm):
    score = IntegerField('Score: ', validators=[
        DataRequired(message='Please enter a score. (1-5)'),
        NumberRange(min=1, max=5, message='Score must be between 1 and 5')
    ])
    review = TextAreaField('Review: ')
    submit = SubmitField('Submit Review')