'''
Author: MeowKJ
Date: 2023-02-02 15:05:49
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-08 11:50:29
FilePath: /chat-meow/meow/utils/conf.py
'''
import yaml
import logging

from meow.utils.context import baidu_lock
from meow.utils.context import openai_lock
from meow.utils.context import audio_lock

import meow.utils.context as mc

def get_conf_data():
    # 打开yaml文件
    logging.debug("***gitting conf data***")
    with open('config.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def get_key_data():
    # 打开yaml文件
    logging.debug("***getting key conf data***")
    with open('key.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data




def set_conf_file(handler, key, value):
    logging.debug("***setting conf data***")
    
    data = get_conf_data()
    data[handler].update({key: value})

    with open('config.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(data, allow_unicode=True))
    return data



def set_conf_data(handler, key, value):
    if handler == 'baidu':
        with baidu_lock:
            set_conf_file('baidu', key, value)
            baidu_handler = mc.get_baidu_handler()
            if hasattr(baidu_handler, key):
                setattr(baidu_handler, key, value)
            else:
                logging.error(f"{key} does not exist")

        return 0
    elif handler == 'openai':
        with openai_lock:
            set_conf_file('openai', key, value)
            openai_handler = mc.get_openai_handler()
            if hasattr(openai_handler, key):
                setattr(openai_handler, key, value)
            else:
                logging.error(f"{key} does not exist")

        return 0
    elif handler == 'audio':
        mc.set_record_stop(True)
        with audio_lock:
            set_conf_file('audio', key, value)
            audio_handler = mc.get_record_handler()
            if hasattr(audio_handler, key):
                setattr(audio_handler, key, value)
            else:
                logging.error(f"{key} does not exist")

        mc.set_record_stop(False)
        return 0
    else:
        logging.error("unspport handler")
        return 1

