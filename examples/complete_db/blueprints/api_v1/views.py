from complete_db.models import Author, Book

import flask_api_framework as af

from .schemas import (
    AuthorsBooksListKwargsSchema,
    AuthorSchema,
    BookCreateSchema,
    BookDetailBodySchema,
    BookDetailKwargsSchema,
    BookListSchema,
)


class AuthorsIndex(af.List, af.Create):
    """
    List all authors.
    Same body schema for List and Create.
    """

    body_schema_cls = AuthorSchema

    def get_instances(self):
        return Author.query.all()


class AuthorsBooksList(af.List):
    """
    List all books for a specific author defined by a view arg.
    """

    kwargs_schema_cls = AuthorsBooksListKwargsSchema
    body_schema_cls = BookListSchema

    def get_instances(self):
        q = Book.query
        q = q.filter_by(author=self.loaded_kwargs)
        return q.all()


class BooksIndex(af.List, af.Create):
    """
    List all books, and Create new book.
    When listing, allow filtering via query params.
    Different body schemas for List and Create.
    """

    list_body_schema_cls = BookListSchema
    create_body_schema_cls = BookCreateSchema

    def get_instances(self):
        return Book.query.all()


class BookDetail(af.Read, af.Update, af.Delete):
    """
    Read, Update, or Delete one specific book.
    Same body schema for Read, Update, Delete.
    """

    kwargs_schema_cls = BookDetailKwargsSchema
    body_schema_cls = BookDetailBodySchema
