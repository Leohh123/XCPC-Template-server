from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, IVCode
from common import fields, marshal_with


class Base(Resource):
    def login(self, name, passwd):
        if current_user.is_authenticated:
            return "already"
        user = db.session.query(User).get(name)
        if user is None or not check_password_hash(user.passwd, passwd):
            return "fail"
        login_user(user, remember=True)
        return "ok"

    def logout(self):
        try:
            logout_user()
            return True
        except:
            return False

    def register(self, name, passwd, ivcode):
        code = db.session.query(IVCode).get(ivcode)
        if code is None:
            return False
        passwd_hash = generate_password_hash(passwd)
        try:
            db.session.add(User(name=name, passwd=passwd_hash))
            db.session.delete(code)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def status(self):
        if current_user.is_authenticated:
            return current_user.name
        return None

    @login_required
    def set_passwd(self, old, new):
        try:
            user = db.session.query(User).get(current_user.name)
            if not check_password_hash(user.passwd, old):
                return False
            new_hash = generate_password_hash(new)
            user.passwd = new_hash
            db.session.commit()
            return True
        except:
            db.rollback()
            return False


parser_login = reqparse.RequestParser()
parser_login.add_argument("name", type=str, required=True)
parser_login.add_argument("passwd", type=str, required=True)


class Login(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_login.parse_args()
        msg = self.login(**args)
        if msg == "ok":
            return "", 0, "Login successfully"
        elif msg == "fail":
            return "", 1, "Login failed"
        elif msg == "already":
            return "", 2, "You have already logged in"
        return "", 3, "Unknown error"


class Logout(Base):
    @marshal_with(fields.Api)
    def get(self):
        flag = self.logout()
        if flag:
            return "", 0, "Logout successfully"
        return "", 1, "Logout failed"


parser_register = reqparse.RequestParser()
parser_register.add_argument("name", type=str, required=True)
parser_register.add_argument("passwd", type=str, required=True)
parser_register.add_argument("ivcode", type=str, required=True)


class Register(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_register.parse_args()
        flag = self.register(**args)
        if flag:
            return "", 0, "Registered successfully"
        return "", 1, "Registration failed"


class Status(Base):
    @marshal_with(fields.Api)
    def get(self):
        res = self.status()
        if res is not None:
            return res, 0, "ok"
        return "", 1, "fail"


parser_set_passwd = reqparse.RequestParser()
parser_set_passwd.add_argument("old", type=str, required=True)
parser_set_passwd.add_argument("new", type=str, required=True)


class SetPasswd(Base):
    @marshal_with(fields.Api)
    def post(self):
        args = parser_set_passwd.parse_args()
        flag = self.set_passwd(**args)
        if flag:
            return "", 0, "Updated successfully"
        return "", 1, "Update failed"
