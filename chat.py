'''
Author: MeowKJ
Date: 2023-02-02 17:15:35
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-08 12:53:47
FilePath: /chat-meow/chat.py
'''
from meow.audio.play import play_from_str
from meow.utils.context import get_record_handler, get_openai_handler, get_baidu_handler
import logging
from meow.utils.context import baidu_lock, openai_lock, audio_lock
from meow.utils.meowinit import generate_handler
import time

from meow.utils.thread import rsgister_chat_thread

def create_chat():
    rsgister_chat_thread(chat_loop)

def chat_loop():
    try:
        generate_handler()
    except Exception as e:
        logging.error(e)
        return
    record_handler = get_record_handler()
    openai_handler = get_openai_handler()
    baidu_handler = get_baidu_handler()
    while True:
        logging.debug('***START_LOOP***')
        logging.info('猫猫正在聆听...')
        code = 1
        audio_lock.acquire()
        code, audio_detect_file = record_handler.detect_audio()
        audio_lock.release()
        while code == 1:
            time.sleep(1)
            with audio_lock:
                code, audio_detect_file = record_handler.detect_audio()
        
        logging.info('猫猫正在理解...')
        # ? 识别
        baidu_lock.acquire()
        code, result_text = baidu_handler.recog(audio_detect_file)
        baidu_lock.release()
        
        logging.info('你说:{}'.format(result_text))

        if not code == 0:
            logging.warning('recognition ERROR, TRY RESTART')
            continue
            
        # ? OPENAI
        openai_lock.acquire()
        code, openai_output = openai_handler.chat(result_text)
        openai_lock.release()
        
        logging.info('猫猫说:{}'.format(openai_output))

        if not code == 0:
            logging.warning('openai ERROR, TRY RESTART')
            continue
        
        # ? 合成
        baidu_lock.acquire()
        code, output_audio = baidu_handler.tts(openai_output)
        baidu_lock.release()
        
        if not code == 0:
            logging.warning('baidu ERROR, TRY RESTART')
        # ? 播放
        try:
            play_from_str(output_audio)
        except Exception as e:
            logging.error('play ERROR, {}'.format(str(e)))

        logging.debug('***END_LOOP***')
