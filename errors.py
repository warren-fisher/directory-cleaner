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


class NotASettingsFile(CustomError):
    """
    Raised when a path leading to a file not of type .pkl is passed into the DirectoryManager
    """
    pass
