from .. import db

from datetime import datetime
import bleach
from markdown import markdown

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text)
    body_html=db.Column(db.Text)
    createtime=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey("users.id"))

    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags=['a','abbr','acronym','b','blockquote','code','em','i',
                      'li','ol','pre','strong','ul','h1','h2','h3','p']
        target.body_html=bleach.linkify(bleach.clean(markdown(value,
                                                              output_format='html'),
                                                     tags=allowed_tags,
                                                     strip=True))

    @staticmethod
    def generate_fake():
        from random import seed, randint;
        from .User import User
        import forgery_py;
        seed()
        user_count = User.query.count()
        for i in range(100):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     createtime=forgery_py.date.date(True), author=u)
            db.session.add(p)
            db.session.commit()

    def to_json(self):
        from .User import User
        json={
            "body":self.body,
            "body_html":self.body_html,
            "id":self.id,
            "createtime":self.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            "author":User.query.get(self.author_id).to_json()
        }
        return json;


db.event.listen(Post.body,"set",Post.on_change_body)


