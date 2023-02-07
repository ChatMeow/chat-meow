'''
Author: MeowKJ
Date: 2023-02-07 17:31:57
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-07 18:02:12
FilePath: /chat-meow/meow/utils/thread.py
'''
from threading import Thread
from meow.utils.context import set_chat_thread
import logging

def rsgister_chat_thread(func):
    chat_thread = Thread(target=func, name='chat_thread')
    chat_thread.setDaemon(True)
    chat_thread.start()
    set_chat_thread(chat_thread)
    logging.info('register chat_thread success')
    
