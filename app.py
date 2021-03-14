from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from database import db, User

from resources import auth, item, link, post, layout

app = Flask(__name__)
app.config.from_json("./config.json")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(name):
    return db.session.query(User).get(name)


api = Api(app)

api.add_resource(auth.Login, "/auth/login", endpoint="auth.login")
api.add_resource(auth.Logout, "/auth/logout", endpoint="auth.logout")
api.add_resource(auth.Register, "/auth/register", endpoint="auth.register")
api.add_resource(auth.Status, "/auth/status", endpoint="auth.status")
api.add_resource(auth.SetPasswd, "/auth/setpasswd", endpoint="auth.setpasswd")

api.add_resource(item.Add, "/item/add", endpoint="item.add")
api.add_resource(item.Delete, "/item/delete", endpoint="item.delete")
api.add_resource(item.Update, "/item/update", endpoint="item.update")
api.add_resource(item.Subitems, "/item/subitems", endpoint="item.subitems")
api.add_resource(item.Query, "/item/query", endpoint="item.query")
api.add_resource(item.Search, "/item/search", endpoint="item.search")

api.add_resource(link.Add, "/link/add", endpoint="link.add")
api.add_resource(link.Delete, "/link/delete", endpoint="link.delete")
api.add_resource(link.Arrange, "/link/arrange", endpoint="link.arrange")

api.add_resource(post.Add, "/post/add", endpoint="post.add")
api.add_resource(post.Apply, "/post/apply", endpoint="post.apply")
api.add_resource(post.Count, "/post/count", endpoint="post.count")
api.add_resource(post.Query, "/post/query", endpoint="post.query")

api.add_resource(layout.Update, "/layout/update", endpoint="layout.update")
api.add_resource(layout.Data, "/layout/data", endpoint="layout.data")
api.add_resource(layout.Error, "/layout/error", endpoint="layout.error")

if __name__ == "__main__":
    app.run(debug=True)
