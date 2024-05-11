from threading import Lock, Thread

from meow.database.db import DBHandler


class AppContext:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AppContext, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # 检查是否已经初始化过
            self.db_manager = None
            self.retry_delay = 10
            self.max_retries = 10
            self.current_retries = 1
            self.baidu_handler = None
            self.oneapi_handler = None
            self.audio_stop = False
            self.chat_thread = None
            self.chat_thread_stop_flag = False
            self.msg = ''
            self.initialized = True  # 设置初始化标志

    def set_handler(self, handler_name, handler):
        with self._lock:
            setattr(self, handler_name, handler)

    def get_handler(self, handler_name):
        with self._lock:
            return getattr(self, handler_name, None)

    def set_db_manager(self, manager):
        self.set_handler('db_manager', manager)

    def get_db_manager(self) -> DBHandler:
        return self.get_handler('db_manager')

    def set_retry_conf(self, delay: int, max_retries: int):
        with self._lock:
            self.retry_delay = delay
            self.max_retries = max_retries

    def set_record_stop(self, stop: bool):
        with self._lock:
            self.audio_stop = stop

    def get_record_stop(self) -> bool:
        with self._lock:
            return self.audio_stop

    def set_chat_thread(self, chat_thread: Thread):
        self.set_handler('chat_thread', chat_thread)

    def get_chat_thread(self) -> Thread:
        return self.get_handler('chat_thread')

    def set_chat_thread_stop_flag(self, flag: bool):
        with self._lock:
            self.chat_thread_stop_flag = flag

    def get_chat_thread_stop_flag(self) -> bool:
        with self._lock:
            return self.chat_thread_stop_flag

    def set_msg(self, m):
        with self._lock:
            self.msg = m

    def get_msg(self):
        with self._lock:
            return self.msg


context = AppContext()


class ThreadStopException(Exception):
    pass


def get_baidu_handler():
    return None
