from flask_wtf import FlaskForm
from wtforms import FileField,HiddenField,StringField,DateField,RadioField,TextAreaField,SubmitField
from wtforms.validators import Email
class EditProfileForm(FlaskForm):
    #可修改昵称 头像 生日 邮箱地址 性别 自我简介
    headimg = FileField("上传头像")
    headkey = HiddenField("头像上传后生成的key")
    nickname = StringField("昵称")
    birthday = DateField("出生日期")
    email = StringField("邮箱地址", validators=[Email()])
    gender = RadioField("性别", choices=[(0, "男"), (1, "女")], default=0,coerce=int)
    remark = TextAreaField("自我简介")
    submit = SubmitField("提交")