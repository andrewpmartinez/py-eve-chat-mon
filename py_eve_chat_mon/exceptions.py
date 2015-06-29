
class EveChatMonException(Exception):
    """Base class for all exceptions

        Attributes:
            message -- An explanation of the error
    """
    message = None

    def __init__(self, message):
        self.message = message


class InvalidChatDirectory(EveChatMonException):
    """Exception raised when the supplied path to Eve's chat log directory is invalid.

        Attributes:
            path -- The invalid path provided
            message -- An explanation of the error
    """
    def __init__(self, path, message):
        self.path = path
        self.message = message

class InvalidCallable(EveChatMonException):
    """Exception raised when a supplied argument does not support __call__"""
    pass




