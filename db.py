import sqlite3

from errors import LibraryError
from initial_data import initial_data


class Database:
    """Sqlite3 library database, persisted when system gets exited"""

    def __init__(self, conn_name: str):
        self.conn = sqlite3.connect(conn_name)
        self.cur = self.conn.cursor()
        if not self._is_table_created():
            self.create_table()
            self.data = initial_data
        else:
            fetched_data = self.fetch_all_data()
            self.data = self._parse_from_db(data=fetched_data)

    def __del__(self):
        self.sync()

    def create_table(self):
        """Creates library table in database"""
        self.cur.execute(
            "CREATE TABLE library(title TEXT, author TEXT, isbn TEXT, price REAL, quantity_in_stock INTEGER)"
        )

    def fetch_all_data(self):
        """Fetches all book data from library table"""
        res = self.cur.execute(
            "SELECT title, author, isbn, price, quantity_in_stock FROM library"
        )
        data = res.fetchall()
        return data

    def sync(self):
        """Adds all books from program state to database"""
        parsed_data = self._parse_to_db(self.data)
        self.cur.execute("DELETE FROM library")
        self.cur.executemany("INSERT INTO library VALUES(?, ?, ?, ?, ?)", parsed_data)
        self.conn.commit()

    def _parse_from_db(self, data):
        """Parses book data from database to dictionary format"""
        formatted_data = {
            item[2]: {
                "title": item[0],
                "author": item[1],
                "isbn": item[2],
                "price": item[3],
                "quantity_in_stock": item[4],
            }
            for item in data
        }
        return formatted_data

    def _is_table_created(self):
        """Checks if library table already exists in database"""
        table_name = self.cur.execute(
            "SELECT name from sqlite_master WHERE name='library'"
        ).fetchone()
        return table_name is not None

    def _parse_to_db(self, data):
        """Parses program data to database format"""
        parsed_data = [
            (
                book["title"],
                book["author"],
                book["isbn"],
                book["price"],
                book["quantity_in_stock"],
            )
            for book in data.values()
        ]
        return parsed_data


class DatabaseWrapper:
    """Creates unified wrappper for database, in case multiple database types are planned"""

    def __init__(self, db: Database):
        self.db = db

    def get_book(self, isbn: str) -> dict[str, str | float | int]:
        """Retrieves book from data"""
        if isbn not in self.db.data:
            raise LibraryError(f"Book {isbn} is not found!")
        return self.db.data[isbn]

    def filter_books_title_author(
        self, title: str | None = None, author: str | None = None
    ) -> list[dict[str, str | float | int]]:
        """Filters books from data by title and author"""
        if title is None and author is None:
            raise LibraryError("At least one filter should be specified!")

        def matched(
            book: dict[str, str | float | int],
            want_title: str | None = None,
            want_author: str | None = None,
        ):
            """Matches found books by title and author"""
            if (
                want_title is not None
                and want_title.lower() not in book["title"].lower()
            ):
                return False
            if (
                want_author is not None
                and want_author.lower() not in book["author"].lower()
            ):
                return False
            return True

        filtered_books = [
            v
            for _, v in self.db.data.items()
            if matched(book=v, want_title=title, want_author=author)
        ]

        return filtered_books

    def add_book(
        self, title: str, author: str, isbn: str, price: float, quantity_in_stock: int
    ):
        """Adds book to system data"""
        if isbn in self.db.data:
            raise LibraryError(f"Book {isbn} is already in library!")

        self.db.data[isbn] = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price,
            "quantity_in_stock": quantity_in_stock,
        }

    def update_book_quantity(self, isbn: str, new_quantity: int):
        """Updates book's quantity in system data"""
        if new_quantity < 0:
            raise ValueError()
        if isbn not in self.db.data:
            raise LibraryError(f"Book {isbn} is not found!")

        self.db.data[isbn]["quantity_in_stock"] = new_quantity

    def del_book(self, isbn: str):
        """Deletes book from system"""
        try:
            self.db.data.pop(isbn)
        except KeyError:
            raise LibraryError(f"Book {isbn} is not found!")

    def list_books(self) -> list[dict[str, str | float | int]]:
        """Returns all books from system"""
        return list(self.db.data.values())
