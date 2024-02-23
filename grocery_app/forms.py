from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_bcrypt import Bcrypt
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import ItemCategory, GroceryStore, User

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

bcrypt = Bcrypt(app)
class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    # Add the following fields to the form class:
    # - title - StringField
    title = StringField('Title', validators=[DataRequired()])
    # - address - StringField
    address = StringField('Address', validators=[DataRequired()])
    # - submit button
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    # Add the following fields to the form class:
    # - name - StringField
    name = StringField('Title', validators=[DataRequired()])
    # - price - FloatField
    price = FloatField('Price')
    # - category - SelectField (specify the 'choices' param)
    category = SelectField('Category', choices=ItemCategory.choices())
    # - photo_url - StringField
    photo_url = StringField('Photo', validators=[URL()])
    # - store - QuerySelectField (specify the `query_factory` param)
    store = QuerySelectField('Stores', query_factory=lambda: GroceryStore.query)
    # - submit button
    submit = SubmitField('Submit')

# -----------------------
class SignUpForm(FlaskForm):
    """Sign Up"""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validate Username"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

# -----------------------
class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        """Validate Username"""
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        """Validate Password"""
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
