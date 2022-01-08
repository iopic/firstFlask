from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email


class DocumentUploadForm(FlaskForm):
    document = FileField('Document', validators=[FileRequired(), FileAllowed(['csv'], 'CSV Document only!')])
    #submit = SubmitField('Submit bia')

class Inputs(FlaskForm):
    myChoices = [(1,"a"),(2,"b")]
    myField = SelectField(u'Variable to view', choices = myChoices, validators = [DataRequired()])

