import mmh3
import re
from datetime import datetime

def parse_msg(msg):
    line_parser = re.compile('^\s*\[\s(.*?)\s\]\s(.*?)\s>\s(.*?)$')
    match = line_parser.match(msg)
    if match:
        timestamp = match.group(1)
        username = match.group(2)
        message = match.group(3)
        message_hash = mmh3.hash(message)
        timestamp = datetime.strptime(timestamp, "%Y.%m.%d %H:%M:%S")

        parsed_msg = {"timestamp": timestamp,
                      "username": username,
                      "message": message,
                      "line": msg,
                      "hash": message_hash}
        return parsed_msg

    return None

class EveChatLogReader(object):
    chat_line_delimiter = u"\ufeff"

    def __init__(self, path):
        self.path = path
        self.file_handle = open(path, "r", encoding="utf-16-le")
        self.file_handle.read(None)

    def read_messages(self):
        buffer = self.file_handle.read(None)
        clean_messages = []
        if buffer:
            messages = buffer.split(EveChatLogReader.chat_line_delimiter)
            for i in range(len(messages)):
                if messages[i] and messages[i] != '':
                    msg = messages[i].replace(EveChatLogReader.chat_line_delimiter, '')
                    msg = re.sub('\s*$', '', msg)
                    clean_messages.append(msg)

        return clean_messages

    def destroy(self):
        self.file_handle.close()
