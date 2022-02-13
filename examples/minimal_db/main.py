from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from flask_api_framework import ApiFramework


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)
af = ApiFramework(app, db)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))


db.create_all()


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        sqla_session = db.session
        load_instance = True


class Books(af.Create, af.List):
    body_schema = BookSchema()

    def get_instances(self):
        return Book.query.all()


app.add_url_rule("/books", view_func=Books.as_view("index"))
