'''
Author: MeowKJ
Date: 2023-02-01 13:04:11
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 18:20:13
FilePath: /ChatMeow/meow/utils/context.py
'''
from threading import Lock

context = {
    'db.manager': None,
    'retry.timewait': 10,
    'retry.max_retries': 10,
    'retry.current_retries': 1,
    'baidu_handler': None,
    'openai_handler': None,
    'audio_handler': None,
    'audio.stop': False
}

baidu_lock = Lock()
openai_lock = Lock()
audio_lock = Lock()


def set_baidu_handler(baidu_handler):
    context.update({'baidu_handler': baidu_handler})


def set_openai_handler(openai_handler):
    context.update({'openai_handler': openai_handler})


def set_audio_handler(audio_handler):
    context.update({'audio_handler': audio_handler})


def get_baidu_handler():
    return context.get('baidu_handler')


def get_openai_handler():

    return context.get('openai_handler')


def get_audio_handler():
    return context.get('audio_handler')


def set_db_manager(db_manager):
    context.update({'db_manager': db_manager})


def get_db_manager():
    return context.get('db_manager')


def set_retries(timewait: int, max_retries: int):
    context.update({'retry.max_retries': max_retries})
    context.update({'retry.timewait': timewait})


def set_audio_stop(stop: bool):
    context.update({'audio.stop': stop})


def get_audio_stop() -> bool:
    return context.get('audio.stop')
