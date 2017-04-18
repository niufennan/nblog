from .. import db


class Role(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),unique=True)
    users=db.relationship("User",backref='role')
    default=db.Column(db.Boolean)
    admin=db.Column(db.Boolean,default=False)
    @staticmethod
    def insert_roles():
        roles={
            "User":('普通用户',True,False),
            "Administrator":("管理员用户",False,True)
        }
        for r in roles:
            print(r)
            role=Role.query.filter_by(name=r[0]).first()
            if role is None:
                role=Role()
            role.name=roles[r][0]
            role.default=roles[r][1]
            role.admin=roles[r][2]
            db.session.add(role)
        db.session.commit()
