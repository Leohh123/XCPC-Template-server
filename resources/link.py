from flask_restful import Resource, reqparse
from flask_login import login_required
from database import db, Item, ItemLink, Constant
from common import fields, marshal_with
import json


class Base(Resource):
    @login_required
    def add(self, src, dst):
        try:
            db.session.add(ItemLink(src=src, dst=dst))
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @login_required
    def delete(self, src, dst):
        try:
            link = db.session.query(ItemLink).get((src, dst))
            db.session.delete(link)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @login_required
    def arrange(self, data):
        try:
            links = json.loads(data)
            length = len(links)
            for index, link in enumerate(links):
                cur_link = db.session.query(ItemLink).get(link)
                cur_link.rank = length - index
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


parser_add = reqparse.RequestParser()
parser_add.add_argument("src", type=int, required=True)
parser_add.add_argument("dst", type=int, required=True)


class Add(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_add.parse_args()
        flag = self.add(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_delete = reqparse.RequestParser()
parser_delete.add_argument("src", type=int, required=True)
parser_delete.add_argument("dst", type=int, required=True)


class Delete(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_add.parse_args()
        flag = self.delete(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_arrange = reqparse.RequestParser()
parser_arrange.add_argument("links", type=str, required=True)


class Arrange(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_arrange.parse_args()
        flag = self.arrange(args["links"])
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"
