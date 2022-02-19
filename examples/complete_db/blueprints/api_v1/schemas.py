from complete_db.ext import ma
from complete_db.models import Author, Book


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True

    id = ma.Integer(dump_only=True)
    name = ma.String()


class AuthorsBooksListKwargsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True

    id = ma.auto_field(data_key="author_id", required=True)


class BookListSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.Integer()
    author = ma.Nested(AuthorSchema())
    title = ma.String()
    year = ma.Integer()
    description = ma.String()


class BookCreateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    author_id = ma.Integer(required=True)
    title = ma.String(required=True)
    year = ma.Integer(required=True)
    description = ma.String()


class BookDetailKwargsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.Integer(required=True)


class BookDetailBodySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.Integer(dump_only=True)
    title = ma.String(required=True)
    year = ma.Integer(required=True)
    description = ma.String(required=True)
