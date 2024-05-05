import logging


from meow.ai.ai import OneapiHandler

from meow.baidu.baidu import BaiduHandler
from meow.audio.record import RecordHandler
from meow.database.db import DBHandler

from meow.utils.conf import get_conf_data, get_key_data

from meow.utils.context import context
def generate_handler():
    context.set_handler('oneapi_handler', None)
    context.set_handler('baidu_handler', None)
    context.set_handler('record_handler', None)

    conf_data = get_conf_data()
    key_data = get_key_data()

    # logging.debug(conf_data)

    openai_config = conf_data['oneapi']
    baidu_config = conf_data['baidu']
    audio_config = conf_data['audio']
    one_api_key = key_data['ONE_API_KEY']
    baidu_key = key_data['BAIDU_KEY']

    logging.info('load conf data finished')

    retry_conf = conf_data['retry']
    context.set_retry_conf(retry_conf['time_delay'], retry_conf['max_retries'])
    logging.info('[1/5]Retry config set')

    record = RecordHandler(**audio_config)
    context.set_handler('record_handler', record)
    logging.info('[2/5]RecordHandler registered')

    oneapi = OneapiHandler(one_api_key, **openai_config)
    context.set_handler('oneapi_handler', oneapi)
    logging.info('[3/5]OpenaiHandler registered')

    baidu = BaiduHandler(*baidu_key, **baidu_config)
    context.set_handler('baidu_handler', baidu)
    logging.info('[4/5]BaiduHandler registered')

    db = DBHandler('database.sqlite')
    context.set_db_manager(db)
    logging.info('[5/5]DBHandler registered')
