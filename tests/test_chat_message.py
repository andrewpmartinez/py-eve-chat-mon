from unittest import TestCase, mock
from unittest.mock import MagicMock, call
from datetime import datetime
from py_eve_chat_mon.chat_message import parse_msg, EveChatLogReader

MESSAGE_SINGLE_LINE = "[ 2015.03.05 21:04:03 ] Some Dude > MSG"
MESSAGE_MULTI_LINE = "[ 2015.03.05 21:04:03 ] Some Dude > MSG\nON NEXT LINE\nANOTHER LINE"

MESSAGE_WITH_TRAILING_WHITE = "[ 2015.03.05 21:04:03 ] Some Dude > MSG\nON NEXT LINE\nANOTHER LINE\n\n\n   "
MESSAGE_WITH_BOMS = EveChatLogReader.chat_line_delimiter.join(["[ 2015.03.05 21:04:03 ] Some Dude > MSG ",
                                                               " middle ",
                                                               " end msg"])

READ_MULTI_MESSAGES = EveChatLogReader.chat_line_delimiter.join(['', MESSAGE_SINGLE_LINE, MESSAGE_MULTI_LINE])
READ_SINGLE_MESSAGES = EveChatLogReader.chat_line_delimiter.join(['', MESSAGE_SINGLE_LINE])


class TestParseMsg(TestCase):
    def setUp(self):
        pass

    def test_parse_msg_returns_non_on_invalid_msg(self):
        result = parse_msg("asdfasdf asldkfj alksdfj ;alskdfj")
        self.assertIsNone(result)

    @mock.patch('py_eve_chat_mon.chat_message.hash')
    def test_parse_msg_parses_single_line_msg(self, mock_md5):
        mock_md5.return_value = "10"
        result = parse_msg(MESSAGE_SINGLE_LINE)

        self.assertEqual(datetime(2015, 3, 5, 21, 4, 3), result['timestamp'])
        self.assertEqual("Some Dude", result['username'])
        self.assertEqual("MSG", result['message'])
        self.assertEqual(MESSAGE_SINGLE_LINE, result['line'])
        self.assertEqual("10", result['hash'])

    @mock.patch('py_eve_chat_mon.chat_message.hash')
    def test_parse_msg_parses_multi_line_msg(self, mock_md5):
        mock_md5.return_value = "10"
        result = parse_msg(MESSAGE_MULTI_LINE)

        self.assertEqual(datetime(2015, 3, 5, 21, 4, 3), result['timestamp'])
        self.assertEqual("Some Dude", result['username'])
        self.assertEqual("MSG\nON NEXT LINE\nANOTHER LINE", result['message'])
        self.assertEqual(MESSAGE_MULTI_LINE, result['line'])
        self.assertEqual("10", result['hash'])

    @mock.patch('py_eve_chat_mon.chat_message.hash')
    def test_parse_calls_md5_with_proper_msg(self, mock_md5):
        line = "[ 2015.03.05 21:04:03 ] Some Dude > MSG\nON NEXT LINE\nANOTHER LINE"

        parse_msg(line)

        mock_md5.assert_called_with("MSG\nON NEXT LINE\nANOTHER LINE")

class TestEveChatLogReader(TestCase):

    def setUp(self):
        self._patch_open = mock.patch('py_eve_chat_mon.chat_message.open', create=True)
        self._mock_open = self._patch_open.start()

    def tearDown(self):
        self._patch_open.stop()

    def test_init_sets_path(self):
        sut = EveChatLogReader("path")

        self.assertEqual("path", sut.path)

    def test_init_opens_with_correct_path(self):
        sut = EveChatLogReader("path")

        self._mock_open.assert_called_with('path', 'r', encoding='utf-16-le')

    def test_init_reads_file_to_end(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()

        sut = EveChatLogReader("path")

        file_handle.read.assert_called_with(None)

    def test_destroy_closes_file_handle(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.close = MagicMock()

        sut = EveChatLogReader("path")
        sut.destroy()

        file_handle.close.assert_called_once()

    def test_read_message_reads_to_end(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()

        calls = []

        for i in range(file_handle.read.call_count + 1):
            calls.append(call(None))

        sut = EveChatLogReader("path")
        sut.read_messages()

        file_handle.read.assert_has_calls(calls)

    def test_read_message_splits_single_message(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()
        file_handle.read.return_value = READ_SINGLE_MESSAGES

        sut = EveChatLogReader("path")
        messages = sut.read_messages()

        self.assertEqual(1, len(messages))
        self.assertEqual(MESSAGE_SINGLE_LINE, messages[0])

    def test_read_message_splits_multiple_messages(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()
        file_handle.read.return_value = READ_MULTI_MESSAGES

        sut = EveChatLogReader("path")
        messages = sut.read_messages()

        self.assertEqual(2, len(messages))
        self.assertEqual(MESSAGE_SINGLE_LINE, messages[0])
        self.assertEqual(MESSAGE_MULTI_LINE, messages[1])

    def test_read_message_cleans_trailing_white_space(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()
        file_handle.read.return_value = MESSAGE_WITH_TRAILING_WHITE

        sut = EveChatLogReader("path")
        messages = sut.read_messages()

        self.assertEqual("[ 2015.03.05 21:04:03 ] Some Dude > MSG\nON NEXT LINE\nANOTHER LINE", messages[0])

    def test_read_message_cleans_boms(self):
        file_handle = self._mock_open.return_value = MagicMock()
        file_handle.read = MagicMock()
        file_handle.read.return_value = MESSAGE_WITH_BOMS

        sut = EveChatLogReader("path")
        messages = sut.read_messages()

        self.assertFalse(EveChatLogReader.chat_line_delimiter in messages[0])
