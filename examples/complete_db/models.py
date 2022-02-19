from complete_db.ext import db
from sqlalchemy.orm import relationship


class Author(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))

    books = relationship("Book", back_populates="author")


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer())
    description = db.Column(db.Text())

    author_id = db.Column(db.Integer(), db.ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")
