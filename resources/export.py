from flask_restful import Resource, reqparse
from flask_login import login_required
from database import db, Item, Post, Constant
from common import fields, marshal_with, config
import json
import re


class Base(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = []
        self.isolated = []

    def get_layout(self):
        self.layout = json.loads(
            db.session.query(Constant).get("layout").value)
        self.isolated = json.loads(db.session.query(
            Constant).get("layout_err").value)["isolated"]

    @login_required
    def latex(self):
        try:
            self.get_layout()

            def escape(s, prefix=None):
                p_block = re.compile(r"```([\S\s]*?)```")
                p_inline = re.compile(r"`(.*?)`")
                p_image = re.compile(r"!\[[\S\s]*?\]\(([\S\s]+?)\)")
                s = p_block.sub(
                    r"\n\\begin{lstlisting}[aboveskip=0pt,belowskip=0pt]\1\\end{lstlisting}", s)
                s = p_inline.sub(r"\\lstinline`\1`", s)
                s = p_image.sub(
                    r"\\includegraphics\[width=\\linewidth\]\{\1\}", s)
                if prefix is not None:
                    s = "\\textbf{{{}}}\\hspace{{0.125cm}}{}".format(prefix, s)
                return s

            def code_block(s):
                p_lang = re.compile(r"^\[language=(\S+?)\](\n|\r|(\n\r))")
                m = p_lang.match(s)
                if m is not None:
                    s = p_lang.sub("", s)
                    return "\\begin{{lstlisting}}[language={}]\n{}\n\\end{{lstlisting}}".format(m.group(1), s)
                return "\\begin{{lstlisting}}\n{}\n\\end{{lstlisting}}".format(s)

            def dfs(item, depth, number):
                it = db.session.query(Item).get(item["id"])
                post = db.session.query(Post).get(it.post_id)
                result = ""
                if it.display and post is not None:
                    if post.description.strip():
                        result += "\n\n" + \
                            escape(post.description.strip(),
                                   prefix="Description:")
                    if post.usage.strip():
                        result += "\n\n" + \
                            escape(post.usage.strip(), prefix="Usage:")
                    if post.complexity.strip():
                        result += "\n\n" + \
                            escape(post.complexity.strip(), prefix="Time:")
                    if post.code.strip():
                        result += "\n\n" + code_block(post.code.strip())
                index = 0
                for subitem in item["items"]:
                    tmp_res = dfs(subitem, depth + 1,
                                  "{}.{}".format(number, index + 1))
                    if tmp_res.strip():
                        result += tmp_res
                        index += 1
                if result.strip():
                    result = "\n\n" + config.LATEX_LEVEL[min(depth, len(
                        config.LATEX_LEVEL) - 1)](it.name, number) + result
                return result

            content = config.LATEX_TEMPLATE_PREV
            index = 0
            for item in self.layout:
                tmp = dfs(item, 0, str(index + 1))
                if tmp.strip():
                    content += tmp
                    index += 1
            return (content + config.LATEX_TEMPLATE_NEXT).strip()
        except:
            db.session.rollback()
            return None


class Latex(Base):
    @marshal_with(fields.Api)
    def get(self):
        result = self.latex()
        if result is not None:
            return result, 0, "ok"
        return "", 1, "fail"
