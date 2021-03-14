from flask_restful import Resource
from flask_login import login_required
from database import db, Item, ItemLink, Constant
from common import fields, marshal_with
import json


class Base(Resource):
    @login_required
    def update(self):
        try:
            items = db.session.query(Item).all()
            links = db.session.query(ItemLink).order_by(
                ItemLink.rank.desc()).all()
            item_dict = {item.id: item for item in items}
            edges = {item.id: [] for item in items}
            indeg = {item.id: 0 for item in items}
            vis = {item.id: False for item in items}
            for link in links:
                edges[link.src].append(link)
                indeg[link.dst] += 1
            result, back_edges, ignored, isolated = [], [], [], []

            def get_res(cur_id):
                cur_res = {
                    "name": item_dict[cur_id].name,
                    "id": cur_id,
                    "items": []
                }
                vis[cur_id] = True
                for link in edges[cur_id]:
                    if not vis[link.dst]:
                        cur_res["items"].append(get_res(link.dst))
                    else:
                        back_edges.append([cur_id, link.dst])
                return cur_res

            for id in indeg:
                if indeg[id] == 0:
                    tmp_res = get_res(id)
                    result.append(tmp_res)
                    if len(edges[id]) == 0:
                        item = item_dict[id]
                        isolated.append({"id": item.id, "name": item.name})
            for id in vis:
                if not vis[id]:
                    item = item_dict[id]
                    ignored.append({"id": item.id, "name": item.name})
            mp = db.session.query(Constant).get("layout")
            mp.value = json.dumps(result)
            err = db.session.query(Constant).get("layout_err")
            err.value = json.dumps({
                "back_edges": back_edges,
                "ignored": ignored,
                "isolated": isolated
            })
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @login_required
    def data(self):
        try:
            return json.loads(db.session.query(Constant).get("layout").value)
        except:
            return None

    @login_required
    def error(self):
        try:
            return json.loads(db.session.query(Constant).get("layout_err").value)
        except:
            return None


class Update(Base):
    @marshal_with(fields.Api)
    def get(self):
        flag = self.update()
        if flag:
            return "", 0, "Updated successfully"
        return "", 1, "Update failed"


class Data(Base):
    @marshal_with(fields.Api)
    def get(self):
        result = self.data()
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"


class Error(Base):
    @marshal_with(fields.Api)
    def get(self):
        result = self.error()
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"
