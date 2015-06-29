import os
import re
import mmh3
import datetime
import logging
import sys
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from .exceptions import InvalidChatDirectory, InvalidCallable

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.debug("DEBUG is ON")

class Monitor:
    """An Eve chat monitor"""

    chats = []
    log_dir = None
    watchdog_observer = None
    event_handler = None
    file_handlers = {}
    max_diff = datetime.timedelta(minutes=5)
    chat_line_delimiter = u"\ufeff"
    trailing_new_lines_match = re.compile('\n*$')
    leading_white_space = re.compile('^\s*')

    #[ 2015.02.02 03:35:20 ] Dakkath Naus > SHIME, Skeleton Crew gang in our catch pocket. I think they're blops,
    # g1 timestamp
    # g2 pilot name
    # g3 msg
    line_parser = re.compile('^\s*\[\s(.*?)\s\]\s(.*?)\s>\s(.*?)$')

    chat_file_parser = re.compile('^(.*?)_\d+_\d+\.')

    def __init__(self, chats, eve_chat_log_dir):
        if not os.path.exists(eve_chat_log_dir):
            raise InvalidChatDirectory(eve_chat_log_dir, "The path '{0}' does not exist.".format(eve_chat_log_dir))

        if not os.path.isdir(eve_chat_log_dir):
            raise InvalidChatDirectory(eve_chat_log_dir,
                                       "The path '{0}' does not point to a directory.".format(eve_chat_log_dir))
        self.chats = chats

        print("Getting started!")
        log_dir = os.path.join(eve_chat_log_dir, '')
        event_handler = ChatLogEventHandler(self.handle_file_changed,
                                            self.handle_file_changed,
                                            self.handle_file_remove,
                                            self.handle_file_remove)

        self.watchdog_observer = Observer()
        self.watchdog_observer.schedule(event_handler, log_dir, recursive=False)

    def start(self):
        self.watchdog_observer.start()

    def stop(self):
        self.watchdog_observer.stop()

    def handle_file_changed(self, event):
        logging.debug("handle_file_changed: start")
        if event.is_directory:
            logging.debug("handle_file_changed: event was for directory")
            return

        file_name = os.path.split(event.src_path)[1]
        matches = self.chat_file_parser.match(file_name)

        if matches and matches.group(1) in self.chats:
            logging.debug("handle_file_changed: file name matched: {0}".format(matches.group(1)))
            if event.src_path not in self.file_handlers:
                logging.debug("handle_file_changed: handler created")
                self.file_handlers[event.src_path] = open(event.src_path, "r", encoding='utf-16-le')

            self.read(self.file_handlers[event.src_path])

        logging.debug("handle_file_changed: end")

    def handle_file_remove(self, event):
        logging.debug("handle_file_remove: start")
        if event.src_path in self.file_handlers:
            logging.debug("handle_file_remove: removing handler")
            self.file_handlers[event.src_path].close()
            del self.file_handlers[event.src_path]

        logging.debug("handle_file_remove: end")

    def read_line(self, file_handle):

        byte = file_handle.read(1)
        byte_line = []
        while byte and byte != self.chat_line_delimiter:
            byte_line.append(byte)
            byte = file_handle.read(1)

        return "".join(byte_line)

    def read(self, file_handle):
        logging.debug("read: start")

        if file_handle.tell() == 0:
            # discard starting BOM
            file_handle.read(1)

        line = self.read_line(file_handle)

        while line:
            line = self.trailing_new_lines_match.sub('', line)
            line = self.leading_white_space.sub('', line)
            line = line.replace(self.chat_line_delimiter, '')
            print(line)
            line_event = self.parse_line(line)

            if line_event:
                logging.debug("read: line parsed")
                now = datetime.datetime.now()
                diff = now - line_event['timestamp']

                if diff <= Monitor.max_diff:
                    logging.debug("read: event dispatched")
                    self.dispatch(line_event)

            line = file_handle.readline()

        logging.debug("read: line was None")
        return None

    def parse_line(self, line):
        logging.debug("parse_line: start")
        match = self.line_parser.match(line)
        if match:
            logging.debug("parse_line: line matched")
            timestamp = match.group(1)
            username = match.group(2)
            message = match.group(3)
            message_hash = mmh3.hash(message)
            timestamp = datetime.datetime.strptime(timestamp, "%Y.%m.%d %H:%M:%S")

            line_event = {"timestamp": timestamp, "username": username, "message": message, "line": line, "hash": message_hash}
            logging.debug("parse_line: end with line matched")
            return line_event

        logging.debug("parse_line: end with NO MATCH: '{0}'".format(line))
        return None

    def dispatch(self, event):
        print(event)


class ChatLogEventHandler(FileSystemEventHandler):
    new_file_callable = None
    file_changed_callable = None
    file_moved_callable = None
    file_deleted_callable = None

    def __init__(self, new_file_callable, file_changed_callable, file_moved_callable, file_deleted_callable):
        """

            :rtype : A new chat log event handler.
        """
        if not hasattr(new_file_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('newFileCallable'))

        if not hasattr(file_changed_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('fileChangedCallable'))

        if not hasattr(file_moved_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('file_moved_callable'))

        if not hasattr(file_deleted_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('file_deleted_callable'))

        self.new_file_callable = new_file_callable
        self.file_changed_callable = file_changed_callable
        self.file_moved_callable = file_moved_callable
        self.file_deleted_callable = file_deleted_callable

    def on_created(self, event):
        logging.debug("On created fired {0}".format(event.src_path))
        self.new_file_callable(event)

    def on_modified(self, event):
        logging.debug("On modified fired {0}".format(event.src_path))
        self.file_changed_callable(event)

    def on_deleted(self, event):
        logging.debug("On deleted fired {0}".format(event.src_path))
        self.file_deleted_callable(event)

    def on_moved(self, event):
        logging.debug("On moved fired {0}".format(event.src_path))
        self.file_removed_callable(event)

