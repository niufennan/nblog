import  os
class Config:
    SECRET_KEY="Niu_blog String"
    SQLALCHEMY_DATABASE_URI=os.environ.get("nblog_mysql_str")  #'mysql://root:1234@localhost/cblog?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    LOGIN_PROTECTION="strong"
    LOGIN_VIEW="login"
    POSTS_PER_PAGE=20


