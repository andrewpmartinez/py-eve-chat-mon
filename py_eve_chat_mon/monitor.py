import threading
from time import sleep
from .chat_directory import EveChatLogDirectoryMonitor
from .chat_message import parse_msg

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
        self.is_alive = False
        self.thread = None

    def start(self):
        self.is_alive = True
        self.thread = threading.Thread(target=self.poll)
        self.thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def poll(self):
        while self.is_alive:
            for chat in self.chats:
                messages = self.chat_log_monitor.read_messages(chat)

                for message in messages:
                    self.handler(chat, parse_msg(message))
            sleep(self.poll_rate)



