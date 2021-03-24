from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class putNewReviewForm(FlaskForm):
    product_id = IntegerField('Product id', validators=[DataRequired()])
    title = StringField('Review title', validators=[DataRequired(), Length(min=1, max=512)])
    review = TextAreaField('Text of review', validators=[DataRequired(), Length(min=1, max=9192)])
    submit = SubmitField('Add new review')