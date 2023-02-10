'''
Author: MeowKJ
Date: 2023-01-25 15:40:12
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-07 17:57:19
FilePath: /chat-meow/meow/baidu/baidu.py
'''

# coding=utf-8
import json
import base64
import time
from meow.utils.retry import network_retry
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import logging
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
ASR_URL = 'http://vop.baidu.com/server_api'
TTS_URL = 'http://tsn.baidu.com/text2audio'

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
timer = time.perf_counter

class BaiduHandler():
    def __init__(self, api_key, secret_key, cuid, dev_pid=1537, per=4, spd=5, pit=5, vol=5):
        self.dev_pid = dev_pid
        # self.scope = scope
        self.api_key = api_key
        self.secret_key = secret_key
        self.cuid = cuid
        self.per = per
        self.spd = spd
        self.pit = pit
        self.vol = vol
        self.format = "pcm"
        self.save_path = "./audio/"
        self.tts_format = "wav"
        self.get_token()

    @network_retry
    def get_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.api_key,
                  'client_secret': self.secret_key}

        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            #logging.error('Baidu token http response http code : ' + str(err.code))
            #logging.error('百度语音识别获取token网络异常, http码为: ' + str(err.code))
            # result_str = err.read()
            logging.error('BAIDU NET ERROR -> Baidu token http response http error: ' + str(err))
            return 1, 'network error'
        result_str = result_str.decode()

        result = json.loads(result_str)
        if 'access_token' in result.keys():
            # # SCOPE = False 忽略检查
            # if self.scope and (not self.scope in result['scope'].split(' ')):
            #     raise Exception('scope is not correct')
            logging.debug('SUCCESS GET BAIDU TOKEN {}. EXPIRES IN SECONDS {}'.format(result['access_token'], result['expires_in']))
            self.token = result['access_token']
            return 0, 'ok'
        else:
            logging.error('NO BAIDU TOKEN -> can not get baidu token in result {}'.format(result_str))
            return 2, 'connot find'

    @network_retry
    def recog(self, speech_data):
            length = len(speech_data)
            if length == 0:
                logging.error('SEECH DATA IS EMPTY -> the baidu speech data to be recognized is empty')
                return 2, 'restart'
            speech = base64.b64encode(speech_data)
            speech = str(speech, 'utf-8')
            params = {'dev_pid': self.dev_pid,
                    'format': self.format,
                    'rate': 16000,
                    'token': self.token,
                    'cuid': self.cuid,
                    'channel': 1,
                    'speech': speech,
                    'len': length
                    }
            post_data = json.dumps(params, sort_keys=False)
            req = Request(ASR_URL, post_data.encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            try:
                begin = timer()
                f = urlopen(req)
                result_str = f.read()
                logging.debug("Request time cost %f" % (timer() - begin))
            except URLError as err:
                logging.error('BAIDU RECOG NETWORK ERROR -> baidu recognition error, asr http response http error : ' + str(err))
                return 1, 'retry'

            result_str = str(result_str, 'utf-8')
            text = dict(json.loads(result_str))["result"][0]
            logging.debug('recognition result: {}'.format(text))
            if(text == ''):
                return 2, 'NO RESULT'
            return 0, text

    @network_retry
    def tts(self, text):
        tex = quote_plus(text)  # 此处TEXT需要两次urlencode
        params = {'tok': self.token, 'tex': tex, 'per': self.per, 'spd': self.spd, 'pit': self.pit, 'vol': self.vol, 'aue': 6, 'cuid': self.cuid,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
        data = urlencode(params)
        req = Request(TTS_URL, data.encode('utf-8'))
        # has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            logging.error('BAIDU TTS NETWORK ERROR -> baidu tts error, asr http response http error : ' + str(err))
            return 1, 'retry'
        logging.debug('TTS OK, result len: %d', len(result_str))
        return 0, result_str
