import yaml
import logging
from meow.database.db import DatabaseManager

from meow.audio.record import AudioBase
from meow.baidu.baidu_audio import BaiduAudio
from meow.ai.openai_api import ChatMeow
import meow.utils.context as mc

from meow.utils.context import baidu_lock
from meow.utils.context import openai_lock
from meow.utils.context import audio_lock


def init_context():
    generate_all_context()

def get_conf_data():
    # 打开yaml文件
    logging.debug("***获取CONFIG文件数据***")
    with open('config.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def get_key_data():
    # 打开yaml文件
    logging.debug("***获取KEY文件数据***")
    with open('key.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def generate_all_context():

    conf_data = get_conf_data()
    # logging.debug(conf_data)
    
    openai_config = conf_data['openai']
    baidu_config = conf_data['baidu']
    audio_config = conf_data['audio']
    
    key_data = get_key_data()

    openai_api_key = key_data['OPENAI_API_KEY']
    baidu_key = key_data['BAIDU_KEY']

    audio = AudioBase(**audio_config)
    openai = ChatMeow(openai_api_key, **openai_config)
    baidu = BaiduAudio(*baidu_key, **baidu_config)

    mc.set_openai_handler(openai)
    mc.set_baidu_handler(baidu)
    mc.set_audio_handler(audio)

    retry_conf = conf_data['retry']
    mc.set_retries(
        retry_conf['timewait'], retry_conf['max_retry_times'])

    db = DatabaseManager('database.sqlite')
    mc.set_db_manager(db)


def set_conf_file(handler, key, value):
    logging.debug("***设置yaml文件数据***")
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
                logging.error(f"{key}不存在")
        return 0
    elif handler == 'openai':
        with openai_lock:
            set_conf_file('openai', key, value)
            openai_handler = mc.get_openai_handler()
            if hasattr(openai_handler, key):
                setattr(openai_handler, key, value)
            else:
                logging.error(f"{key}不存在")
        return 0
    elif handler == 'audio':
        mc.set_audio_stop(True)
        with audio_lock:
            set_conf_file('audio', key, value)
            audio_handler = mc.get_audio_handler()
            if hasattr(audio_handler, key):
                setattr(audio_handler, key, value)
            else:
                logging.error(f"{key}不存在")
        mc.set_audio_stop(False)
        return 0
    else:
        logging.error("不支持的handler")
        return 1

