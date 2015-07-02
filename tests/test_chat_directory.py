from os import path
from unittest import TestCase
from unittest.mock import MagicMock, patch
from datetime import datetime
from py_eve_chat_mon.chat_directory import DirChangeEventHandler, get_chat_from_file_name, get_existing_logs, \
    get_timestamp_from_file_name
from py_eve_chat_mon.exceptions import InvalidCallable, InvalidChatDirectory

INVALID_PATH = path.join('.', 'I', 'DO', 'NOT', 'EXIST', '123232')
FILE_PATH = path.join('.', __file__)

class TestGetTimestampFromFileName(TestCase):

    def test_invalid_format_returns_none(self):
        result = get_timestamp_from_file_name("some_file_20150404_234df.txt")
        self.assertIsNone(result)

    def test_valid_format_returns_proper_timestamp(self):
        result = get_timestamp_from_file_name("some_file_20150404_234536.txt")
        self.assertEqual(datetime(2015, 4, 4, 23, 45, 36), result)


class TestGetChatFromFileName(TestCase):

    def test_invalid_format_returns_none(self):
        result = get_chat_from_file_name("some_file_20150404_234df.txt")
        self.assertIsNone(result)

    def test_valid_format_returns_proper_chat_name(self):
        result = get_chat_from_file_name("some_file_20150404_234536.txt")
        self.assertEqual('some_file', result)


class TestGetExistingLogs(TestCase):

    def test_invalid_path_raises_exception(self):
        self.assertRaises(InvalidChatDirectory, get_existing_logs, INVALID_PATH)

    def test_file_path_raises_exception(self):
        self.assertRaises(InvalidChatDirectory, get_existing_logs, FILE_PATH)

    @patch('py_eve_chat_mon.chat_directory.os')
    def test_valid_path_returns_proper_chats(self, mock_os):
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.isfile.return_value = True

        mock_os.listdir.return_value = [
            'chat_one_20150404_234536.txt',
            'chat_two_20150130_065423.txt'
        ]

        chats = get_existing_logs('some/path')

        self.assertTrue('chat_one' in chats)
        self.assertTrue('chat_two' in chats)

    @patch('py_eve_chat_mon.chat_directory.os')
    def test_valid_path_returns_proper_chat_paths(self, mock_os):
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.isfile.return_value = True

        mock_os.path.join = path.join

        mock_os.listdir.return_value = [
            'chat_one_20150404_234536.txt',
            'chat_two_20150130_065423.txt'
        ]

        base_path = path.join('some', 'path')
        chat_one_path = path.join(base_path, 'chat_one_20150404_234536.txt')
        chat_two_path = path.join(base_path, 'chat_two_20150130_065423.txt')

        chats = get_existing_logs(base_path)

        self.assertEqual(chat_one_path, chats['chat_one']['path'])
        self.assertEqual(chat_two_path, chats['chat_two']['path'])

    @patch('py_eve_chat_mon.chat_directory.os')
    def test_valid_path_returns_proper_chat_timestamps(self, mock_os):
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.isfile.return_value = True

        mock_os.path.join = path.join

        mock_os.listdir.return_value = [
            'chat_one_20150404_234536.txt',
            'chat_two_20150130_065423.txt'
        ]

        base_path = path.join('some', 'path')

        chats = get_existing_logs(base_path)

        chat_one_timestamp = datetime(2015, 4, 4, 23, 45, 36)
        chat_two_timestamp = datetime(2015, 1, 30, 6, 54, 23)

        self.assertEqual(chats['chat_one']['timestamp'], chat_one_timestamp)
        self.assertEqual(chats['chat_two']['timestamp'], chat_two_timestamp)


class TestEveChatLogDirectoryMonitor(TestCase):

    def test_init_invalid_path_raises_exception(self):
        pass

    def test_init_file_path_raises_exception(self):
        pass

    def test_init(self):
        pass

    def test_init_creates_dir_event_handler_with_proper_call_backs(self):
        pass

    def test_init_adds_existing_chats(self):
        pass

    def test_init_get_existing_chats(self):
        pass

    def test_init_creates_observer(self):
        pass

    def test_init_schedules_observer(self):
        pass

    def test_read_messages_reads_from_added_chat(self):
        pass

    def test_read_messages_returns_none_for_non_added_chat(self):
        pass

    def test_remove_chat_log_calls_destroy_on_chat_reader(self):
        pass

    def test_remove_chat_log_removes_chat_reader_entry(self):
        pass

    def test_add_chat_log_calls_remove_first(self):
        pass

    def test_add_chat_log_creates_new_chat_reader_with_path(self):
        pass

    def test_add_chat_log_registers_chat_reader_entry(self):
        pass

    def test_on_delete_does_nothing_for_directory_events(self):
        pass

    def test_on_delete_removes_the_proper_chat(self):
        pass

    def test_on_create_does_nothing_for_directory_events(self):
        pass

    def test_on_create_adds_the_proper_chat_and_path(self):
        pass


class TestDirChangeEventHandler(TestCase):

    def setUp(self):

        self._on_create = MagicMock()
        self._on_delete = MagicMock()

        self._sut = DirChangeEventHandler(self._on_create, self._on_delete)

    def test_init_raises_exception_if_new_file_is_not_callable(self):
        self.assertRaises(InvalidCallable, DirChangeEventHandler, 1, lambda x: x)

    def test_init_raises_exception_if_file_delete_is_not_callable(self):
        self.assertRaises(InvalidCallable, DirChangeEventHandler, lambda x: x, 1)

    def test_init(self):
        self.assertEqual(self._on_create, self._sut.new_file_callable)
        self.assertEqual(self._on_delete, self._sut.file_deleted_callable)

    def test_on_create_calls_proper_handler(self):
        event = {}
        self._sut.on_created(event)

        self._on_create.assert_called_once_with(event)

    def test_on_delete_calls_proper_handler(self):
        event = {}
        self._sut.on_deleted(event)

        self._on_delete.assert_called_once_with(event)
