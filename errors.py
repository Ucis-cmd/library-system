class LibraryError(Exception):
    """Exception for library and book related errors"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
