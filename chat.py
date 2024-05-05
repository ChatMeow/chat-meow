import logging
import time

from meow.utils.meowinit import generate_handler
from meow.utils.thread import register_chat_thread
from meow.utils.context import context


def create_chat():
    register_chat_thread(chat_loop)


def chat_loop():
    try:
        generate_handler()
    except Exception as e:
        logging.error(e)
        return
    record_handler = context.get_handler('record_handler')
    openai_handler = context.get_handler('oneapi_handler')
    baidu_handler = context.get_handler('baidu_handler')
    baidu_recognition_failed_times = 0
    baidu_tts_failed_times = 0
    openai_failed_times = 0
    while True:
        logging.debug('***START_LOOP***')
        if baidu_recognition_failed_times > 10 or baidu_tts_failed_times > 10 or openai_failed_times > 10:
            raise 'ERROR GET MAX FAILED, CHECK NETWORK OR KEY'

        logging.info('猫猫正在聆听...')

        code, audio_detect_file = record_handler.detect_audio()
        while code == 1:
            time.sleep(1)
            code, audio_detect_file = record_handler.detect_audio()

        logging.info('猫猫正在理解...')
        # ? 识别
        code, result_text = baidu_handler.recog(audio_detect_file)

        context.set_msg('你说:{}'.format(result_text))
        logging.info('你说:{}'.format(result_text))

        if not code == 0:
            logging.warning('recognition ERROR, TRY RESTART times{}'.format(baidu_recognition_failed_times))
            baidu_recognition_failed_times += 1
            continue
        else:
            baidu_recognition_failed_times = 0

        # ? OPENAI
        code, openai_output = openai_handler.chat(result_text)

        context.set_msg('猫猫说:{}'.format(openai_output))

        logging.info('猫猫说:{}'.format(openai_output))

        if not code == 0:
            logging.warning('openai ERROR, TRY RESTART times{}'.format(openai_failed_times))
            openai_failed_times += 1
            continue
        else:
            openai_failed_times = 0

        # ? ? ? ? 喇叭预热
        record_handler.before_play_from_str()

        # ? 合成
        code, output_audio = baidu_handler.tts(openai_output)

        if not code == 0:
            logging.warning('baidu ERROR, TRY RESTART times{}'.format(baidu_tts_failed_times))
            baidu_recognition_failed_times += 1
        else:
            baidu_recognition_failed_times = 0

        # ? 播放
        try:
            record_handler.play_from_str(output_audio)
        except Exception as e:
            logging.error('play ERROR, {}'.format(str(e)))
            raise Exception('ERROR STOP when Play')

        logging.debug('***END_LOOP***')
