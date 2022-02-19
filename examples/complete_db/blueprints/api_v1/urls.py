from . import views
from .blueprint import bp


bp.add_url_rule(
    rule="/authors",
    endpoint="authors_index",
    view_func=views.AuthorsIndex.as_view("authors_index"),
)
bp.add_url_rule(
    rule="/authors/<author_id>/books",
    endpoint="authors_books_list",
    view_func=views.AuthorsBooksList.as_view("authors_books_list"),
)
bp.add_url_rule(
    rule="/books",
    endpoint="books_index",
    view_func=views.BooksIndex.as_view("books_index"),
)
bp.add_url_rule(
    rule="/books/<id>",
    endpoint="book_detail",
    view_func=views.BookDetail.as_view("book_detail"),
)
