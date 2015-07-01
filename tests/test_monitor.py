import unittest.mock
from os import path
from unittest import TestCase, mock
from py_eve_chat_mon.monitor import Monitor
from py_eve_chat_mon.exceptions import InvalidChatDirectory, InvalidMonitorState


class TestMonitor(TestCase):
    def setUp(self):
        self._chats = ['Alliance', 'Corp']
        self._valid_path = "."
        self._invalid_path = path.join(".", "I", "wont", "exist", "ever", "123")
        self._handler = unittest.mock.MagicMock(return_value=None)
        self._poll_rate = 0

        self._patcher_eve_chat_log_dir_mon = mock.patch('py_eve_chat_mon.monitor.EveChatLogDirectoryMonitor')
        self._mock_monitor = self._patcher_eve_chat_log_dir_mon.start()

        self._patch_parse_msg = mock.patch('py_eve_chat_mon.monitor.parse_msg')
        self._mock_parse_msg = self._patch_parse_msg.start()

        self._patch_sleep = mock.patch('py_eve_chat_mon.monitor.sleep')
        self._mock_sleep = self._patch_sleep.start()

        self._patch_thread = mock.patch('py_eve_chat_mon.monitor.Thread')
        self._mock_thread_instance = self._patch_thread.start()
        self._mock_thread_instance.stop = unittest.mock.MagicMock(name="stop")
        self._mock_thread_instance.start = unittest.mock.MagicMock(name="start")

        self._sut = Monitor(self._chats, self._valid_path, self._handler, self._poll_rate)

    def tearDown(self):
        self._patcher_eve_chat_log_dir_mon.stop()
        self._patch_parse_msg.stop()
        self._patch_sleep.stop()
        self._patch_thread.stop()

    def test_init_bad_path_errors(self):
        self._patcher_eve_chat_log_dir_mon.stop()

        self.failUnlessRaises(InvalidChatDirectory, Monitor, self._chats, self._invalid_path, self._handler,
                              self._poll_rate)

        self._patcher_eve_chat_log_dir_mon.start()

    def test_init(self):
        self.assertEqual(self._chats, self._sut.chats)
        self.assertEqual(self._handler, self._sut.handler)
        self.assertFalse(self._sut.is_alive)
        self.assertIsNone(self._sut.thread)
        self.assertEqual(self._poll_rate, self._sut.poll_rate)

        self._mock_monitor.assert_called_once_with(self._valid_path)

    def test_stop_throws_exception_on_not_alive(self):
        self.assertRaises(InvalidMonitorState, self._sut.stop)

    def test_stop_sets_is_alive_false(self):
        self._sut.start()
        self._sut.stop()

        self.assertFalse(self._sut.is_alive)

    def test_stop_stops_thread(self):
        self._sut.start()
        self._sut.stop()

        self._mock_thread_instance.stop.assert_called_once()

    def test_stop_sets_thread_none(self):
        self._sut.start()
        self._sut.stop()

        self.assertIsNone(self._sut.thread)

    def test_start_throws_exception_on_alive(self):
        self._sut.start()

        self.assertRaises(InvalidMonitorState, self._sut.start)

    def test_start_sets_is_alive(self):
        self._sut.start()

        self.assertTrue(self._sut.is_alive)

    def test_start_creates_new_thread(self):
        self._sut.start()

        self._mock_thread_instance.assert_called_once()

    def test_start_creates_new_thread_with_specified_poll_interval(self):
        self._sut.start()

        self._mock_thread_instance.assert_called_once_with(target=self._sut.poll)

    def test_start_sets_thread_to_daemon(self):
        self._sut.start()

        self.assertTrue(self._sut.thread.daemon)

    def test_start_starts_new_thread(self):
        self._sut.start()

        self._mock_thread_instance.start.assert_called_once()

    def test_poll_calls_sleep_with_poll_rate(self):
        self._sut._should_poll = unittest.mock.MagicMock(side_effect=[True, False])
        self._sut.poll()

        self._mock_sleep.assert_called_with(self._poll_rate)

    def test_poll_checks_each_chat(self):
        self._sut._should_poll = unittest.mock.MagicMock(side_effect=[True, False])
        self._sut.chat_log_monitor.read_messages = unittest.mock.MagicMock()
        self._sut.chat_log_monitor.read_messages.return_value = []
        self._sut.poll()

        calls = [unittest.mock.call(self._chats[0]), unittest.mock.call(self._chats[1])]

        # noinspection PyUnresolvedReferences
        self._sut.chat_log_monitor.read_messages.assert_has_calls(calls)

    def test_poll_parses_each_chats_messages(self):
        self._sut._should_poll = unittest.mock.MagicMock(side_effect=[True, False])
        self._sut.chat_log_monitor.read_messages = unittest.mock.MagicMock()
        self._sut.chat_log_monitor.read_messages.return_value = ["1", "2"]
        self._sut.poll()

        calls = [unittest.mock.call("1"), unittest.mock.call("2"), unittest.mock.call("1"), unittest.mock.call("2")]

        self._mock_parse_msg.assert_has_calls(calls)

    def test_poll_calls_handler_with_chat_and_parsed_msg(self):
        self._sut._should_poll = unittest.mock.MagicMock(side_effect=[True, False])
        self._sut.chat_log_monitor.read_messages = unittest.mock.MagicMock()
        self._sut.chat_log_monitor.read_messages.return_value = ["1", "2"]
        self._mock_parse_msg.side_effect = ["p1", "p2", "p3", "p4"]
        self._sut.poll()

        calls = [unittest.mock.call(self._chats[0], "p1"), unittest.mock.call(self._chats[0], "p2"),
                 unittest.mock.call(self._chats[1], "p3"), unittest.mock.call(self._chats[1], "p4")]

        self._handler.assert_has_calls(calls)
