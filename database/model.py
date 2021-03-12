from .db import db
from datetime import datetime


class User(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    passwd = db.Column(db.String(256), nullable=False)
    posts = db.relationship("Post", backref="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name


class IVCode(db.Model):
    code = db.Column(db.String(16), primary_key=True)


class Test(db.Model):
    a = db.Column(db.String(8), primary_key=True)
    b = db.Column(db.String(8), nullable=False)
    c = db.Column(db.String(16), nullable=False)
    d = db.Column(db.Text, nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    post_id = db.Column(db.Integer, nullable=False, default=-1)
    display = db.Column(db.Boolean, nullable=False, default=True)


class ItemLink(db.Model):
    src = db.Column(db.Integer, db.ForeignKey("item.id"), primary_key=True)
    dst = db.Column(db.Integer, db.ForeignKey("item.id"), primary_key=True)
    rank = db.Column(db.Integer, nullable=False, default=0)
    src_item = db.relationship("Item", foreign_keys=[src])
    dst_item = db.relationship("Item", foreign_keys=[dst])


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    complexity = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(32), db.ForeignKey(
        "user.name"), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Constant(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    value = db.Column(db.Text, nullable=False)
