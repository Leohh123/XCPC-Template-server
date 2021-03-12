from flask_restful import Resource, reqparse, inputs
from flask_login import login_required
from database import db, Item, ItemLink, Post
from common import fields, marshal_with, config


class Base(Resource):
    @login_required
    def add(self, name, src=None):
        try:
            item = Item(name=name)
            db.session.add(item)
            if src is not None:
                src_item = db.session.query(Item).get(src)
                if src_item is None:
                    return False
                db.session.flush()
                db.session.add(ItemLink(src=src, dst=item.id))
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @login_required
    def delete(self, id):
        try:
            db.session.query(ItemLink).filter(
                (ItemLink.src == id) | (ItemLink.dst == id)).delete()
            item = db.session.query(Item).get(id)
            db.session.delete(item)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @login_required
    def update(self, id, name=None, post_id=None, display=None):
        try:
            item = db.session.query(Item).get(id)
            if name is not None:
                item.name = name
            if post_id is not None:
                item.post_id = post_id
            if display is not None:
                item.display = display
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def subitems(self, cur_id):
        try:
            res = db.session.query(ItemLink.dst, Item.name) \
                .join(Item, ItemLink.dst == Item.id) \
                .order_by(ItemLink.rank).filter(ItemLink.src == cur_id).all()
            return res
        except:
            db.session.rollback()
            return None

    def query(self, id):
        try:
            item = db.session.query(Item).get(id)
            post = db.session.query(Post).get(item.post_id)
            if post is None:
                post = Post(**config.POST_TEMPLATE)
            return {
                "name": item.name,
                "post": post,
                "display": item.display
            }
        except:
            db.session.rollback()
            return None

    def search(self, keyword):
        try:
            items = db.session.query(Item).filter(
                Item.name.contains(keyword)).all()
            return items
        except:
            db.session.rollback()
            return None


parser_add = reqparse.RequestParser()
parser_add.add_argument("name", type=str, required=True)
parser_add.add_argument("src", type=int)


class Add(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_add.parse_args()
        flag = self.add(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_delete = reqparse.RequestParser()
parser_delete.add_argument("id", type=int, required=True)


class Delete(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_delete.parse_args()
        flag = self.delete(args["id"])
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_update = reqparse.RequestParser()
parser_update.add_argument("id", type=int, required=True)
parser_update.add_argument("name", type=str)
parser_update.add_argument("post_id", type=int)
parser_update.add_argument("display", type=inputs.boolean)


class Update(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_update.parse_args()
        flag = self.update(**args)
        if flag:
            return "", 0, "ok"
        return "", 1, "fail"


parser_subitems = reqparse.RequestParser()
parser_subitems.add_argument("id", type=int, required=True)
fields_subitems = fields.Api(fields.List(fields.Layout({
    "id": fields.Integer(attr=0),
    "name": fields.String(attr=1)
})))


class Subitems(Base):
    @marshal_with(fields_subitems)
    def post(self):
        args = parser_subitems.parse_args()
        result = self.subitems(args["id"])
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"


parser_query = reqparse.RequestParser()
parser_query.add_argument("id", type=int, required=True)
fields_query = fields.Api(fields.Layout({
    "name": fields.String,
    "display": fields.Boolean,
    "post": fields.Model({
        "id": fields.Integer,
        "title": fields.String,
        "description": fields.String,
        "usage": fields.String,
        "complexity": fields.String,
        "code": fields.String,
        "note": fields.String,
        "author": fields.String,
        "time": fields.Datetime
    })
}))


class Query(Base):
    @marshal_with(fields_query)
    def post(self):
        args = parser_query.parse_args()
        result = self.query(args["id"])
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"


parser_search = reqparse.RequestParser()
parser_search.add_argument("keyword", type=str, required=True)
fields_search = fields.Api(fields.List(fields.Model({
    "value": fields.String(attr="name"),
    "id": fields.Integer
})))


class Search(Base):
    @marshal_with(fields_search)
    def get(self):
        args = parser_search.parse_args()
        result = self.search(args["keyword"])
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"
