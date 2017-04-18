from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,RadioField,DateField,\
    TextAreaField,FileField,HiddenField
from wtforms.validators import DataRequired,EqualTo,Length,Email,ValidationError
from ..models.User import User

class RegisterForm(Form):
    username = StringField("请输入用户名", validators=[Length(6,16),DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    repassword=PasswordField("确认密码", validators=[EqualTo("password")])
    headimg=FileField("上传头像")
    headkey=HiddenField("头像上传后生成的key")
    nickname= StringField("昵称")
    birthday= DateField("出生日期")
    email= StringField("邮箱地址", validators=[Email()])
    gender= RadioField("性别", choices=[("0", "男"), ("1", "女")], default=0)
    remark= TextAreaField("自我简介")
    submit=SubmitField("提交")

    def validate_username(self, field):
        if (User.query.filter_by(username=field.data).first()):
            raise ValidationError("此用户名已经使用！")