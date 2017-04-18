from flask_login import UserMixin,AnonymousUserMixin
from  ..  import db,login_manager
from .Role import Role
from .Post import Post
from .Follow import Follow
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,index=True)
    password=db.Column(db.String(50))
    nickname=db.Column(db.String(50))
    email=db.Column(db.String(100))
    birthday=db.Column(db.DateTime)
    gender=db.Column(db.Integer)
    headimg = db.Column(db.String(50))
    remark=db.Column(db.String(200))
    lastseen=db.Column(db.DateTime,default=datetime.utcnow)
    createtime=db.Column(db.DateTime,default=datetime.utcnow)
    role_id=db.Column(db.Integer,db.ForeignKey("roles.id"))
    posts=db.relationship("Post",backref="author",lazy='dynamic')

    #关注我的
    followers=db.relationship("Follow",foreign_keys=[Follow.followed_id],
                             backref=db.backref("followed",lazy='joined'),lazy="dynamic",
                             cascade="all,delete-orphan")
    #我关注的
    followed = db.relationship("Follow", foreign_keys=[Follow.follower_id],
                               backref=db.backref("follower", lazy='joined'), lazy="dynamic",
                               cascade="all,delete-orphan")

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first();

    def is_administrator(self):
        return self.role is not None and self.role.admin

    def visit(self):
        self.lastseen=datetime.utcnow()
        db.session.add(self);
    #关注用户
    def follow(self,user):
        if(not self.is_following(user)):
            f=Follow(follower=self,followed=user)
            db.session.add(f);
    #取消关注
    def unfollow(self,user):
        f=self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f);

    #我是否关注此用户
    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None;
    #此用户是否关注了我
    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None;

    def followed_posts(user):
        return db.session.query(Post).select_from(Follow).filter_by(follower_id=user.id).join(Post,Follow.followed_id == Post.author_id)

    def to_json(self):
        json = {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "email": self.email,
            "birthday": self.birthday,
            "gender": self.gender,
            "headimg": self.headimg,
            "remark":self.remark,
            "createtime": self.createtime.strftime('%Y-%m-%d %H:%M:%S')
        };
        return json;

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser