'''
Author: MeowKJ
Date: 2023-02-02 17:15:35
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-06 19:41:49
FilePath: /chat-meow/chat.py
'''
from meow.audio.play import play
from meow.utils.context import get_audio_handler, get_openai_handler, get_baidu_handler
import logging
from meow.utils.context import baidu_lock, openai_lock, audio_lock
from meow.utils.conf import init_context
import time

def chat_loop():
    init_context()
    audio_handler = get_audio_handler()
    openai_handler = get_openai_handler()
    baidu_handler = get_baidu_handler()
    while True:
        logging.info('***START_LOOP***')
        code = 1
        audio_lock.acquire()
        code, audio_detect_file = audio_handler.detect_audio()
        audio_lock.release()
        while code == 1:
            time.sleep(1)
            with audio_lock:
                code, audio_detect_file = audio_handler.detect_audio()

        
        # ? 识别
        baidu_lock.acquire()
        code, result_text = baidu_handler.recog(audio_detect_file)
        baidu_lock.release()
        
        if not code == 0:
            logging.warning('recognition ERROR, TRY RESTART')
            continue
            
        # ? OPENAI
        openai_lock.acquire()
        code, openai_output = openai_handler.chat(result_text)
        openai_lock.release()
        
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
            play(output_audio)
        except Exception as e:
            logging.error('play ERROR, %s'.format(e))

        logging.info('***END_LOOP***')
