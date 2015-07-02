from unittest import TestCase



class TestGetTimestampFromFileName(TestCase):

    def test_invalid_format_returns_none(self):
        pass

    def test_valid_format_returns_proper_timestamp(self):
        pass


class TestGetChatFromFileName(TestCase):

    def test_invalid_format_returns_none(self):
        pass

    def test_valid_format_returns_proper_chat_name(self):
        pass


class TestGetExistingLogs(TestCase):

    def test_invalid_path_raises_exception(self):
        pass

    def test_file_path_raises_exception(self):
        pass

    def test_valid_path_returns_proper_chats(self):
        pass

    def test_valid_path_returns_proper_chat_paths(self):
        pass

    def test_valid_path_returns_proper_chat_timestamps(self):
        pass



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

    def test_oncreate_does_nothing_for_directory_events(self):
        pass

    def test_on_create_adds_the_proper_chat_and_path(self):
        pass


class TestDirChangeEventHandler(TestCase):

    def test_init_raises_exception_if_new_file_is_not_callable(self):
        pass

    def test_init_raises_exception_if_file_delete_is_not_callable(self):
        pass

    def test_init(self):
        pass

    def test_on_create_calls_proper_handler(self):
        pass

    def test_on_delete_calls_proper_handler(self):
        pass

