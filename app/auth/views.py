from . import auth
from .. import  db,login_manager
from ..forms.LoginForm import LoginForm
from ..forms.RegisterForm import RegisterForm
from ..models.User import User
from flask_login import login_user,logout_user,current_user
from flask import  render_template,flash,redirect,url_for

@auth.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    print(url_for("main.index"))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            print(url_for("main.index"))
            return redirect(url_for("main.index"))
        else:
            flash("您输入的用户名或密码错误")
            return render_template("/auth/login.html", form=form)  # 返回的仍为登录页
        return redirect(url_for("main.index"))
    return render_template("/auth/login.html",form=form)

@auth.route("/logout",methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for("main.index"))

#注册
@auth.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User()
        user.username=form.username.data
        user.password=form.password.data
        user.birthday=form.birthday.data
        user.email=form.email.data
        user.headimg=form.headkey.data
        user.gender=form.gender.data
        user.nickname=form.nickname.data
        user.remark=form.remark.data
        db.session.add(user)
        db.session.commit()
        login_user(user);
        return redirect(url_for("main.index"))
    return  render_template("/auth/register.html",form=form)
@auth.before_app_request
def before_request():
    if(current_user.is_authenticated):
        current_user.visit()

@login_manager.user_loader
def load_user(user_id):
    print(user_id);
    return User.query.get(int(user_id))
