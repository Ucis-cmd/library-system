# library-system
Simple library management system with books

## Getting started
```py
uv venv # Add virtual environment
uv pip install -r requirements.txt # Install dependencies 
uv run main.py # Run library system
```

## Modules
- db.py - Database module
- errors.py - Custom exceptions (only LibraryError)
- handlers.py - UI and Database connector
- ui.py - UI (terminal) of program
- main.py - Executable (main) file
