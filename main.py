from rich.console import Console
from db import Database, DatabaseWrapper

from ui import UI
from handlers import BookHandler

# Configurable system-wide variables
STYLE_COLOR = "cyan"
DB_CONNECTION_NAME = "library.db"


def main() -> None:
    console = Console()
    ui = UI(console=console, color=STYLE_COLOR)
    db = Database(conn_name=DB_CONNECTION_NAME)
    db_interface = DatabaseWrapper(db=db)
    handler = BookHandler(ui=ui, db_interface=db_interface)

    # Action list used for UI and function execution
    actions = {
        "Get book by ISBN": handler.get_book,
        "Find books by title and/or author": handler.get_filtered_books,
        "List all books": handler.list_books,
        "Add book": handler.add_book,
        "Update book's quantity": handler.update_book_quantity,
        "Delete book": handler.del_book,
        "Exit": handler.exit,
    }

    console.rule("THE AMAZING LIBRARY", style=STYLE_COLOR)
    console.print(f"[{STYLE_COLOR} bold]Welcome!!![/{STYLE_COLOR} bold]")

    while True:
        selected_action = ui.list_actions(action_texts=list(actions.keys()))

        if selected_action is None:
            break

        if selected_action == "Exit":
            console.print(
                f"[{STYLE_COLOR} bold on purple]Bye...[{STYLE_COLOR} bold on purple]"
            )
            break
        actions[selected_action]()


main()
