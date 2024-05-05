import yaml
import logging

from meow.utils.context import context

def get_conf_data():
    # 打开yaml文件
    logging.debug("***Getting conf data***")
    with open('config.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def get_key_data():
    # 打开yaml文件
    logging.debug("***Getting key conf data***")
    with open('key.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def set_conf_file(handler, key, value):
    logging.debug("***Setting conf data***")

    data = get_conf_data()
    data[handler].update({key: value})

    with open('config.yml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(data, allow_unicode=True))
    return data


def set_conf_data(handler, key, value):
    if handler == 'baidu':
        set_conf_file('baidu', key, value)
        baidu_handler = context.get_handler('baidu_handler')
        if hasattr(baidu_handler, key):
            setattr(baidu_handler, key, value)
        else:
            logging.error(f"{key} does not exist")

        return 0
    elif handler == 'oneapi':
        set_conf_file('oneapi', key, value)
        oneapi_handler = context.get_handler('oneapi_handler')
        if hasattr(oneapi_handler, key):
            setattr(oneapi_handler, key, value)
        else:
            logging.error(f"{key} does not exist")

        return 0
    elif handler == 'audio':
        context.set_record_stop(True)
        set_conf_file('audio', key, value)
        audio_handler = context.get_handler('audio_handler')
        if hasattr(audio_handler, key):
            setattr(audio_handler, key, value)
        else:
            logging.error(f"{key} does not exist")

        context.set_record_stop(False)
        return 0
    else:
        logging.error("Unsupported handler")
        return 1
