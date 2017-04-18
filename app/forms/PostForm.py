from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired
class PostForm(FlaskForm):
    body=PageDownField("分享一下现在的心情吧！",validators=[DataRequired()])
    submit=SubmitField("分享")