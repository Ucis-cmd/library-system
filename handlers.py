import functools
import re

from errors import LibraryError
from ui import UI
from db import DatabaseWrapper


def handle_errors(fn):
    """Handles library and unexpected errors, logs them to console"""

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except LibraryError as e:
            self.ui.console.print(f"[red]Library error: {e}[/red]")
        except Exception as e:
            self.ui.console.print(f"[red]Unknown exception: {e}[/red]")

    return wrapper


def is_valid_isbn(isbn: str) -> bool:
    return re.match("^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$", isbn)


class BookHandler:
    """Connects ui with database for book related actions"""

    def __init__(self, ui: UI, db_interface: DatabaseWrapper):
        self.ui = ui
        self.db_interface = db_interface

    @handle_errors
    def get_book(self):
        """Retrieves selected book info and prints it"""
        isbn = self.ui.console.input("ISBN: ")
        book = self.db_interface.get_book(isbn)
        self.ui.print_book(book)

    @handle_errors
    def get_filtered_books(self):
        """Retrieves filtered books by title and author (both optional)"""
        title = self.ui.console.input("Title: ")
        author = self.ui.console.input("Author: ")
        books = self.db_interface.filter_books_title_author(title=title, author=author)

        if len(books) == 0:
            self.ui.console.print("No books found!")
            return

        self.ui.list_books(books=books)

    @handle_errors
    def list_books(self):
        """Retrieves all books from db and shows them in UI"""
        books = self.db_interface.list_books()

        if len(books) == 0:
            self.ui.console.print("No books found!")
            return

        self.ui.list_books(books=books)

    @handle_errors
    def add_book(self):
        """Adds book and it's information to db"""
        while True:
            isbn = self.ui.console.input("ISBN: ")
            if not is_valid_isbn(isbn):
                self.ui.console.print("Invalid ISBN format!")
                continue
            break
        title = self.ui.console.input("Title: ")
        author = self.ui.console.input("Author: ")
        while True:
            try:
                price = float(self.ui.console.input("Price: "))
            except ValueError:
                print("Please input a valid price!")
                continue
            break
        while True:
            try:
                quantity = int(self.ui.console.input("Quantity: "))
                if quantity < 0:
                    raise ValueError
            except ValueError:
                print("Please input a valid quantity!")
                continue
            break

        self.db_interface.add_book(
            title=title,
            author=author,
            isbn=isbn,
            price=price,
            quantity_in_stock=quantity,
        )

    @handle_errors
    def update_book_quantity(self):
        """Updates selected book's quantity"""
        isbn = self.ui.console.input("ISBN: ")
        quantity = int(self.ui.console.input("New quantity: "))

        self.db_interface.update_book_quantity(isbn, quantity)

    @handle_errors
    def del_book(self):
        """Deletes selected book from system"""
        while True:
            isbn = self.ui.console.input("ISBN: ")
            if not is_valid_isbn(isbn):
                self.ui.console.print("Invalid ISBN format!")
                continue
            break
        self.db_interface.del_book(isbn=isbn)

    @handle_errors
    def exit(self) -> bool:
        """Stops program"""
        return True
