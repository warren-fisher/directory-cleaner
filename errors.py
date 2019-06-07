class CustomError(Exception):
    """
    Base error class.
    """
    pass

class NotAFileError(CustomError):
    """
    Raised when a filepath does not lead to a file.
    """
    pass

class NotADirectoryError(CustomError):
    """
    Raised when a filepath does not lead to a directory
    """
    pass
