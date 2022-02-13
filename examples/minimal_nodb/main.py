from flask import Flask

from flask_api_framework import ApiFramework


app = Flask(__name__)
af = ApiFramework(app)


class Index(af.Read):
    def get_instance(self):
        return dict(value="minimal")


app.add_url_rule("/", view_func=Index.as_view("index"))
