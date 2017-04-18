from flask_wtf import FlaskForm
from wtforms import FileField,HiddenField,StringField,DateField,RadioField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Email,ValidationError,DataRequired
from ..models.User import User
from ..models.Role import Role
class EditProfileAdminForm(FlaskForm):
    #可修改昵称 头像 生日 邮箱地址 性别 自我简介
    headimg = FileField("上传头像")
    headkey = HiddenField("头像上传后生成的key")
    username=StringField("用户名",validators=[DataRequired()])
    role=SelectField("用户角色",coerce=int)
    nickname = StringField("昵称")
    birthday = DateField("出生日期")
    email = StringField("邮箱地址", validators=[Email()])
    gender = RadioField("性别", choices=[(0, "男"), (1, "女")], default=0,coerce=int)
    remark = TextAreaField("自我简介")
    submit = SubmitField("提交")

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.all()]
        self.user=user;

    def validate_username(self,field):
        if(field.data!=self.username and User.query.filter_by(username=field.data).first()):
            raise ValidationError("此用户名已经使用！")
