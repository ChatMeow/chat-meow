'''
Author: MeowKJ
Date: 2023-01-25 00:57:53
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-07 17:59:52
FilePath: /chat-meow/main.py
'''
from meow.web.app import create_app
from chat import create_chat
import logging

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    create_chat()
    create_app()


