from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from database import db, Post, Item
from common import fields, marshal_with


class Base(Resource):
    @login_required
    def add(self, title, description, usage, complexity, code, note):
        try:
            post = Post(title=title, description=description, usage=usage,
                        complexity=complexity, code=code, note=note, author=current_user.name)
            db.session.add(post)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def apply(self, id, title, description, usage, complexity, code, note):
        try:
            post = Post(title=title, description=description, usage=usage,
                        complexity=complexity, code=code, note=note, author=current_user.name)
            db.session.add(post)
            db.session.flush()
            item = db.session.query(Item).get(id)
            item.post_id = post.id
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


parser_add = reqparse.RequestParser()
parser_add.add_argument("title", type=str, required=True)
parser_add.add_argument("description", type=str, required=True)
parser_add.add_argument("usage", type=str, required=True)
parser_add.add_argument("complexity", type=str, required=True)
parser_add.add_argument("code", type=str, required=True)
parser_add.add_argument("note", type=str, required=True)


class Add(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_add.parse_args()
        flag = self.add(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_apply = reqparse.RequestParser()
parser_apply.add_argument("id", type=int, required=True)
parser_apply.add_argument("title", type=str, required=True)
parser_apply.add_argument("description", type=str, required=True)
parser_apply.add_argument("usage", type=str, required=True)
parser_apply.add_argument("complexity", type=str, required=True)
parser_apply.add_argument("code", type=str, required=True)
parser_apply.add_argument("note", type=str, required=True)


class Apply(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_apply.parse_args()
        flag = self.apply(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"
