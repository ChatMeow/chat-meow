'''
Author: MeowKJ
Date: 2023-02-07 17:31:57
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-10 21:14:58
FilePath: /chat-meow/meow/utils/thread.py
'''
from threading import Thread
from meow.utils.context import set_chat_thread
from meow.utils.context import get_chat_thread
from meow.utils.context import set_chat_thread_stop_flag, audio_lock

import logging

def rsgister_chat_thread(func):
    if((get_chat_thread() is None) or (not get_chat_thread().is_alive())):
        chat_thread = Thread(target=func, name='chat_thread')
        chat_thread.setDaemon(True)
        set_chat_thread_stop_flag(False)
        chat_thread.start()
        set_chat_thread(chat_thread)
        logging.info('register chat_thread success')
    logging.warning('Thread is still running, stop before register')

def stop_chat_thread():
    set_chat_thread_stop_flag(True)
    

