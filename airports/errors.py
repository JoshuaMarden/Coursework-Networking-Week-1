class CustomError(Exception):
    """Base class for custom errors."""
    pass


class APIError(CustomError):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code
        super().__init__(self.message)

    def print_error(self):
        print(f"{self.code}: {self.message}")


class InputError(CustomError):
    """Exception raised for errors in the input."""

    def __init__(self, message="Unexpected user input, input unprocessable"):
        self.message = message
        super().__init__(self.message)
