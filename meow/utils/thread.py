from threading import Thread
from meow.utils.context import context


import logging


def register_chat_thread(func):
    if (context.get_chat_thread() is None) or (not context.get_chat_thread()
                                               .is_alive()):
        chat_thread = Thread(target=func, name='chat_thread', daemon=True)
        context.set_chat_thread_stop_flag(False)
        chat_thread.setDaemon(True)
        chat_thread.start()
        context.set_chat_thread(chat_thread)
        logging.info('register chat_thread success')
    logging.warning('Thread is still running, stop before register')


def stop_chat_thread():
    context.set_chat_thread_stop_flag(True)
