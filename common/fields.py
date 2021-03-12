from database import db
from functools import wraps


def make(cls):
    if isinstance(cls, type):
        return cls()
    return cls


def marshal_with(fields):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            return make(fields).get(func(*args, **kwargs))
        return decorated
    return decorator


class Raw(object):
    def __init__(self, attr=None):
        self.attr = attr


class Empty(object):
    def __init__(self, **kwargs):
        super(Empty, self).__init__(**kwargs)

    def get(self, data):
        return data


class Layout(Raw):
    def __init__(self, shape, **kwargs):
        super(Layout, self).__init__(**kwargs)
        self.shape = shape
        assert isinstance(self.shape, (list, tuple, dict))

    def get(self, data):
        if isinstance(self.shape, (list, tuple)):
            return [make(f).get(data[f.attr]) for f in self.shape]
        res = {}
        for k, f in self.shape.items():
            inst = make(f)
            if inst.attr is not None:
                res[k] = inst.get(data[inst.attr])
            else:
                res[k] = inst.get(data[k])
        return res


class List(Raw):
    def __init__(self, fields, **kwargs):
        super(List, self).__init__(**kwargs)
        self.fields = make(fields)

    def get(self, data):
        return [self.fields.get(d) for d in data]


class Envelope(Raw):
    def __init__(self, title, fields, **kwargs):
        super(Envelope, self).__init__(**kwargs)
        self.fields = make(fields)
        self.title = title
        assert isinstance(self.title, str)

    def get(self, data):
        return dict([[self.title, self.fields.get(data)]])


class Integer(Raw):
    def __init__(self, **kwargs):
        super(Integer, self).__init__(**kwargs)

    def get(self, data):
        return int(data)


class Float(Raw):
    def __init__(self, **kwargs):
        super(Float, self).__init__(**kwargs)

    def get(self, data):
        return float(data)


class Boolean(Raw):
    def __init__(self, **kwargs):
        super(Boolean, self).__init__(**kwargs)

    def get(self, data):
        return bool(data)


class String(Raw):
    def __init__(self, **kwargs):
        super(String, self).__init__(**kwargs)

    def get(self, data):
        return str(data)


class Datetime(Raw):
    def __init__(self, **kwargs):
        super(Datetime, self).__init__(**kwargs)

    def get(self, data):
        return int(data.timestamp() * 1000)


class Model(Raw):
    def __init__(self, shape, **kwargs):
        super(Model, self).__init__(**kwargs)
        self.shape = shape
        assert isinstance(self.shape, (list, tuple, dict))

    def get(self, data):
        assert isinstance(data, db.Model)
        if isinstance(self.shape, (list, tuple)):
            return [make(f).get(getattr(data, f.attr)) for f in self.shape]
        res = {}
        for k, f in self.shape.items():
            inst = make(f)
            if inst.attr is not None:
                res[k] = inst.get(getattr(data, inst.attr))
            else:
                res[k] = inst.get(getattr(data, k))
        return res


class Api(Raw):
    def __init__(self, fields=Empty, **kwargs):
        super(Api, self).__init__(**kwargs)
        self.fields = make(fields)

    def get(self, data):
        assert isinstance(data, (list, tuple)) and len(data) == 3
        assert isinstance(data[1], int) and isinstance(data[2], str)
        res = "" if data[0] == "" else self.fields.get(data[0])
        return {"data": res, "code": data[1], "message": data[2]}


class Any(Raw):
    def __init__(self, func, **kwargs):
        super(Any, self).__init__(**kwargs)
        self.func = func

    def get(self, data):
        return self.func(data)
