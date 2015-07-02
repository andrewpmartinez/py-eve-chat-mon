
class EveChatMonException(Exception):
    """Base class for all exceptions

        Attributes:
            message -- An explanation of the error
    """
    def __init__(self, message):
        super(EveChatMonException, self).__init__(message)

class InvalidChatDirectory(EveChatMonException):
    """Exception raised when the supplied path to Eve's chat log directory is invalid.

        Attributes:
            path -- The invalid path provided
            message -- An explanation of the error
    """
    def __init__(self, path, message):
        super(InvalidChatDirectory, self).__init__(message)
        self.path = path

class InvalidCallable(EveChatMonException):
    """Exception raised when a supplied argument does not support __call__"""
    def __init__(self, message):
        super(InvalidCallable, self).__init__(message)


class InvalidMonitorState(EveChatMonException):
    def __init__(self, message):
        super(InvalidMonitorState, self).__init__(message)
