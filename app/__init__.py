# coding=utf-8
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment
from qiniu import Auth
import pymysql
pymysql.install_as_MySQLdb()
from config import Config
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager=LoginManager();
pagedown=PageDown();
moment=Moment();
access_key=os.environ.get("qn_access_key")
secret_key=os.environ.get("qn_secret_key")
qn=Auth(access_key,secret_key)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection=Config.LOGIN_PROTECTION
    login_manager.login_view=Config.LOGIN_VIEW
    db.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    app.qn=qn;
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .api_1_0 import api as api_bluiprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix="/auth")
    app.register_blueprint(api_bluiprint,url_prefix="/api/v1_0")
    return app


'''
@app.route("/")
def index():
    return render_template("index.html",site_name='myblog')

@app.route("/user/")

@app.route('/user/<name>')
def user(name):
    age=request.args.get("age")
    if name =='test':
        abort(500)
    return "<h1>hello %s!</h1>"%name
    #return " ".join(['hello',name,'! you age is ',age])
@app.route("/req_test")
def req_test():
    val=""
    for key ,value in request.headers.items():
        val+=" %s = %s <br>"  % (key,value)
    return   val

@app.route("/res_test")
def res_test():
    response=make_response("<h1>hello world</h1")
    response.set_cookie("name","niufennan")
    return response;

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            login_user(user,form.remember_me.data)
            return redirect(url_for("index"))
        else:
            flash("您输入的用户名或密码错误")
            return render_template("/login.html",form=form)  # 返回的仍为登录页
    return render_template("/login.html",form=form)

@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User()
        user.username=form.username.data
        user.password=form.password.data
        user.birthday=form.birthday.data
        user.email=form.email.data
        user.gender=form.gender.data
        user.nickname=form.nickname.data
        user.role_id=1          #暂时约定公开用户角色为1
        db.session.add(user)
    return  render_template("/register.html",form=form)

if __name__=='__main__':
    #app.run(debug=True)
    mamager.run()
 '''





