from os import path
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from datetime import datetime
from py_eve_chat_mon.chat_directory import DirChangeEventHandler, get_chat_from_file_name, get_existing_logs, \
    get_timestamp_from_file_name, EveChatLogDirectoryMonitor
from py_eve_chat_mon.exceptions import InvalidCallable, InvalidChatDirectory, ObserverAlreadyAdded

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
    def test_multiple_chat_logs_returns_most_recent(self, mock_os):
        mock_os.path.exists.return_value = True
        mock_os.path.isdir.return_value = True
        mock_os.path.isfile.return_value = True

        mock_os.path.join = path.join

        mock_os.listdir.return_value = [
            'chat_one_20150104_234536.txt',
            'chat_one_20150130_065423.txt'
        ]

        base_path = path.join('some', 'path')
        chat_one_path = path.join(base_path, 'chat_one_20150130_065423.txt')

        chats = get_existing_logs(base_path)

        self.assertEqual(1, len(chats))
        self.assertEqual(chat_one_path, chats['chat_one']['path'])

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

    def setUp(self):
        self._sut = None
        self._patcher_os = patch('py_eve_chat_mon.chat_directory.os')
        self._mock_os = self._patcher_os.start()

        self._mock_os.path.exists.return_value = True
        self._mock_os.path.isdir.return_value = True

        self._patch_watchdog = patch('py_eve_chat_mon.chat_directory.Observer')
        self._mock_watch_dog = self._patch_watchdog.start()

        self._patch_dir_change_event_handler = patch('py_eve_chat_mon.chat_directory.DirChangeEventHandler')
        self._mock_dir_change_event_handler = self._patch_dir_change_event_handler.start()

        self._chat_info = {'chat_one.txt': {'path':  'chat_one_path.txt'},
                           'chat_two.txt': {'path': 'chat_two_path.txt'}}

        self._patch_get_existing_chats = patch('py_eve_chat_mon.chat_directory.get_existing_logs')
        self._mock_get_existing_chats = self._patch_get_existing_chats.start()
        self._mock_get_existing_chats.return_value = self._chat_info

        self._patch_eve_chat_log_reader = patch('py_eve_chat_mon.chat_directory.EveChatLogReader')
        self._mock_eve_chat_log_reader = self._patch_eve_chat_log_reader.start()

    def tearDown(self):
        self._patcher_os.stop()
        self._patch_watchdog.stop()
        self._patch_dir_change_event_handler.stop()
        self._patch_get_existing_chats.stop()
        self._patch_eve_chat_log_reader.stop()

    def test_init_invalid_path_raises_exception(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._patcher_os.stop()
        self.assertRaises(InvalidChatDirectory, EveChatLogDirectoryMonitor, INVALID_PATH)
        self._patcher_os.start()

    def test_init_file_path_raises_exception(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._patcher_os.stop()
        self.assertRaises(InvalidChatDirectory, EveChatLogDirectoryMonitor, FILE_PATH)
        self._patcher_os.start()

    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor._add_file_observer')
    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor._add_existing_log_files')
    def test_init(self, mock_add_log_files, mock_add_file_observer):
        self._sut = EveChatLogDirectoryMonitor("path")

        self.assertEqual("path", self._sut.path)
        self.assertIsNone(self._sut.watchdog_observer)
        self.assertIsNotNone(self._sut.chats)
        self.assertEqual(0, len(self._sut.chats))

        mock_add_log_files.assert_called_once()
        mock_add_file_observer.assert_called_once()

    def test_add_file_observer_raises_exception_on_double_call(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self.assertRaises(ObserverAlreadyAdded, self._sut._add_file_observer)

    def test_add_file_observer_creates_dir_event_handler_with_proper_call_backs(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._mock_dir_change_event_handler.assert_called_with(self._sut.on_create, self._sut.on_delete)

    def test_add_file_observer_creates_observer(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._mock_watch_dog.assert_called_once()

    def test_add_file_observer_sets_watchdog_observer(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self.assertEqual(self._mock_watch_dog(), self._sut.watchdog_observer)

    def test_add_file_observer_schedulers_observer(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._mock_watch_dog().schedule.assert_called_with(self._mock_dir_change_event_handler(),
                                                           self._sut.path,
                                                           recursive=False)

    def test_add_existing_get_existing_chats(self):
        self._sut = EveChatLogDirectoryMonitor("path")
        self._mock_get_existing_chats.assert_called_once_with(self._sut.path)

    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor.add_chat_log')
    def test_add_existing_adds_existing_chats(self, mock_add_chat_log):
        self._sut = EveChatLogDirectoryMonitor("path")

        calls = [call('chat_one.txt', self._chat_info['chat_one.txt']['path']),
                 call('chat_two.txt', self._chat_info['chat_two.txt']['path'])]

        mock_add_chat_log.assert_has_calls(calls, any_order=True)

    def test_read_messages_reads_from_added_chat(self):
        self._mock_eve_chat_log_reader().read_messages.return_value = "MSGS"
        self._sut = EveChatLogDirectoryMonitor("path")

        result = self._sut.read_messages("chat_one.txt")

        self._mock_eve_chat_log_reader().read_messages.assert_has_calls([call()])
        self.assertEqual("MSGS", result)

    def test_read_messages_returns_none_for_non_added_chat(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        result = self._sut.read_messages("fake_chat_name")

        self.assertIsNone(result)

    def test_remove_chat_log_calls_destroy_on_chat_reader(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        self._sut.remove_chat_log("chat_one.txt")

        self._mock_eve_chat_log_reader().destroy.assert_called_once()

    def test_remove_chat_log_removes_chat_reader_entry(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        self._sut.remove_chat_log("chat_one.txt")

        self.assertTrue("chat_one.txt" not in self._sut.chats)

    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor.remove_chat_log')
    def test_add_chat_log_calls_remove_first(self, mock_remove_chat_log):
        self._sut = EveChatLogDirectoryMonitor("path")

        mock_remove_chat_log.reset_mock()

        self._sut.add_chat_log("boom_chat", "path")

        mock_remove_chat_log.assert_called_once_with("boom_chat")

    def test_add_chat_log_creates_new_chat_reader_with_path(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        self._mock_eve_chat_log_reader.reset_mock()

        self._sut.add_chat_log("boom_chat", "super-sweet-path")

        self._mock_eve_chat_log_reader.assert_called_once_with('super-sweet-path')

    def test_add_chat_log_registers_chat_reader_entry(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        self._mock_eve_chat_log_reader.reset_mock()

        self._sut.add_chat_log("boom_chat", "super-sweet-path")

        self.assertTrue("boom_chat" in self._sut.chats)

    def test_on_delete_does_nothing_for_directory_events(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        event = MagicMock()
        event.is_directory = True

        self._mock_os.path.split.reset_mock()

        self._sut.on_delete(event)

        self.assertFalse(self._mock_os.path.split.called)

    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor.remove_chat_log')
    def test_on_delete_removes_the_proper_chat(self, mock_remove_chat_log):
        self._sut = EveChatLogDirectoryMonitor("path")

        event = MagicMock()
        event.is_directory = False
        event.src_path = "some_chat_20150101_240101.txt"

        self._patcher_os.stop()
        mock_remove_chat_log.reset_mock()

        self._sut.on_delete(event)

        self._patcher_os.start()

        mock_remove_chat_log.assert_called_once_with("some_chat")

    def test_on_create_does_nothing_for_directory_events(self):
        self._sut = EveChatLogDirectoryMonitor("path")

        event = MagicMock()
        event.is_directory = True

        self._mock_os.path.split.reset_mock()

        self._sut.on_create(event)

        self.assertFalse(self._mock_os.path.split.called)

    @patch('py_eve_chat_mon.chat_directory.EveChatLogDirectoryMonitor.add_chat_log')
    def test_on_create_adds_the_proper_chat_and_path(self, mock_add_chat_log):
        self._sut = EveChatLogDirectoryMonitor("path")

        event = MagicMock()
        event.is_directory = False
        event.src_path = "some_chat_20150101_240101.txt"

        self._patcher_os.stop()
        mock_add_chat_log.reset_mock()

        self._sut.on_create(event)

        self._patcher_os.start()

        mock_add_chat_log.assert_called_once_with("some_chat", event.src_path)


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
