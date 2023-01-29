from libs.requirements import *

class getPrompt(FlaskForm):
    prompt = StringField('prompt', validators=[DataRequired()])
    submit = SubmitField('Submit')