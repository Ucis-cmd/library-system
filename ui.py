from rich.console import Console
from rich.table import Table
import questionary as qst


class UI:
    """User interface for library system"""

    def __init__(self, console: Console, color: str):
        self.console = console
        self.color = color
        self.style_single_print = f"{self.color} bold"

    def print_book(self, book) -> None:
        """Prints book's data to console"""
        self.console.print("Title: ", book["title"], style=self.style_single_print)
        self.console.print("Author: ", book["author"], style=self.style_single_print)
        self.console.print("ISBN: ", book["isbn"], style=self.style_single_print)
        self.console.print(
            "Price: ",
            f"{book['price']:.2f}[green]$[/green]",
            style=self.style_single_print,
        )
        self.console.print(
            "Quantity: ", book["quantity_in_stock"], style=self.style_single_print
        )

    def list_actions(self, action_texts: list[str]) -> str | None:
        """Lists actions and returns the selected action"""
        res = qst.select("What do you want to do?", choices=action_texts).ask()
        return res

    def list_books(self, books: list) -> None:
        """Lists books to terminal"""
        table = Table(title="Found books")

        table.add_column("Title")
        table.add_column("Author")
        table.add_column("ISBN")
        table.add_column("Price")
        table.add_column("Quantity")

        for book in books:
            table.add_row(
                book["title"],
                book["author"],
                book["isbn"],
                f"{book['price']:.2f}$",
                str(book["quantity_in_stock"]),
            )

        self.console.print(table)
