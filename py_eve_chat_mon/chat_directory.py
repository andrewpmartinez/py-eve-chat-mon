import os
import re
from datetime import datetime
from .chat_message import EveChatLogReader
from .exceptions import InvalidChatDirectory, InvalidCallable, ObserverAlreadyAdded
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_timestamp_from_file_name(file_name):
    chat_file_timestamp_parser = re.compile('.*?_(\d{8}_\d{6})\.txt$')
    matches = chat_file_timestamp_parser.match(file_name)

    if matches:
        return datetime.strptime(matches.group(1), "%Y%m%d_%H%M%S")

    return None


def get_chat_from_file_name(file_name):
    chat_file_name_parser = re.compile('^(.+?)_\d+_\d+\.')
    matches = chat_file_name_parser.match(file_name)

    if matches:
        return matches.group(1)

    return None


def get_existing_logs(path):
    if not os.path.exists(path):
        raise InvalidChatDirectory(path, "The path '{0}' does not exist.".format(path))

    if not os.path.isdir(path):
        raise InvalidChatDirectory(path,
                                   "The path '{0}' does not point to a directory.".format(path))

    existing_chat_logs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    existing_chats = {}

    for file_name in existing_chat_logs:
        chat_name = get_chat_from_file_name(file_name)
        timestamp = get_timestamp_from_file_name(file_name)

        if chat_name in existing_chats:
            if timestamp > existing_chats[chat_name]['timestamp']:
                existing_chats[chat_name] = {'timestamp': timestamp, 'path': os.path.join(path, file_name)}
        else:
            existing_chats[chat_name] = {'timestamp': timestamp, 'path': os.path.join(path, file_name)}

    return existing_chats


class EveChatLogDirectoryMonitor(object):

    def __init__(self, path):
        if not os.path.exists(path):
            raise InvalidChatDirectory(path, "The path '{0}' does not exist.".format(path))

        if not os.path.isdir(path):
            raise InvalidChatDirectory(path,
                                       "The path '{0}' does not point to a directory.".format(path))
        self.path = path
        self.chats = {}
        self.watchdog_observer = None

        self._add_existing_log_files()
        self._add_file_observer()

    def _add_file_observer(self):
        if self.watchdog_observer:
            raise ObserverAlreadyAdded()

        event_handler = DirChangeEventHandler(self.on_create, self.on_delete)

        self.watchdog_observer = Observer()
        self.watchdog_observer.schedule(event_handler, self.path, recursive=False)

    def _add_existing_log_files(self):
        existing_logs = get_existing_logs(self.path)
        for chat_name, file_info in existing_logs.items():
            self.add_chat_log(chat_name, file_info['path'])

    def read_messages(self, chat_name):
        if chat_name in self.chats:
            return self.chats[chat_name].read_messages()

        return None

    def remove_chat_log(self, chat_name):
        if chat_name in self.chats:
            self.chats[chat_name].destroy()
            del self.chats[chat_name]

    def add_chat_log(self, chat_name, path):
        self.remove_chat_log(chat_name)
        self.chats[chat_name] = EveChatLogReader(path)

    def on_delete(self, event):
        if event.is_directory:
            return

        file_name = os.path.split(event.src_path)[1]

        chat_name = get_chat_from_file_name(file_name)

        self.remove_chat_log(chat_name)

    def on_create(self, event):
        if event.is_directory:
            return

        file_name = os.path.split(event.src_path)[1]
        chat_name = get_chat_from_file_name(file_name)

        self.add_chat_log(chat_name, event.src_path)


class DirChangeEventHandler(FileSystemEventHandler):

    def __init__(self, new_file_callable, file_deleted_callable):

        if not hasattr(new_file_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('newFileCallable'))

        if not hasattr(file_deleted_callable, '__call__'):
            raise InvalidCallable("The value passed as '{0}' is not a callable.".format('file_deleted_callable'))

        self.new_file_callable = new_file_callable
        self.file_deleted_callable = file_deleted_callable

    def on_created(self, event):
        self.new_file_callable(event)

    def on_deleted(self, event):
        self.file_deleted_callable(event)


