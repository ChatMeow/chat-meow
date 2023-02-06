'''
Author: MeowKJ
Date: 2023-01-25 00:57:53
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-06 19:43:28
FilePath: /chat-meow/main.py
'''
from threading import Thread
from meow.web.app import create_app
from chat import chat_loop
import logging

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    chat_thread = Thread(target=chat_loop, name='chat_thread')
    chat_thread.setDaemon(True)
    chat_thread.start()
    create_app()


