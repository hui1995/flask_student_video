
from . import db

class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(50),nullable=False)
    uname = db.Column(db.String(30),nullable=False)
    upwd = db.Column(db.String(30),nullable=False)
    def __init__(self,loginname,uname,upwd):
        self.loginname = loginname
        self.uname = uname
        self.upwd = upwd
