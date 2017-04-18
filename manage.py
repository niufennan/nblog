# coding=utf-8

from app import create_app, db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app.models.User import User
from app.models.Role import Role
from app.models.Post import Post

import pymysql
pymysql.install_as_MySQLdb()
app=create_app()
manager=Manager(app);
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post)
manager.add_command("db", MigrateCommand)
manager.add_command("shell" ,Shell(make_context=make_shell_context))

if __name__ =='__main__':
    manager.run()