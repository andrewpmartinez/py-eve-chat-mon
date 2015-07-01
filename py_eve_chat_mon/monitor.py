from threading import Thread
from time import sleep
from .chat_directory import EveChatLogDirectoryMonitor
from .chat_message import parse_msg
from .exceptions import InvalidMonitorState

class Monitor:
    """An Eve chat monitor"""

    def __init__(self, chats, path, handler, poll_rate=2):
        self.chats = chats
        self.chat_log_monitor = EveChatLogDirectoryMonitor(path)
        self.handler = handler
        self.is_alive = False
        self.thread = None
        self.poll_rate = poll_rate

    def stop(self):
        if not self.is_alive:
            raise InvalidMonitorState("Monitor not started")
        self.is_alive = False
        self.thread.stop()
        self.thread = None

    def start(self):
        if self.is_alive:
            raise InvalidMonitorState("Monitor already started")
        self.is_alive = True
        self.thread = Thread(target=self.poll)
        self.thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def _should_poll(self):
        return self.is_alive

    def poll(self):
        while self._should_poll():
            for chat in self.chats:
                messages = self.chat_log_monitor.read_messages(chat)

                for message in messages:
                    self.handler(chat, parse_msg(message))
            sleep(self.poll_rate)



