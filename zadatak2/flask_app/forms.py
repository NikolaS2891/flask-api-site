from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired,InputRequired

class NewSiteInput(FlaskForm):
    
    cell_id = StringField('cell_id', validators=[DataRequired()])
    azimuth = IntegerField('azimuth', validators=[InputRequired()], )
    band = IntegerField('band', validators=[DataRequired()])
    submit = SubmitField('Post')

