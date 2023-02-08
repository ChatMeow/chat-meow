'''
Author: MeowKJ
Date: 2023-02-02 14:41:56
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-08 16:20:29
FilePath: /chat-meow/meow/web/app.py
'''
from flask import Flask, render_template
from flask import request

import logging

from meow.utils.conf import get_conf_data
from meow.utils.conf import set_conf_data
from meow.utils.context import get_chat_thread, get_msg, set_msg, msg_lock
from meow.utils.thread import stop_chat_thread

from chat import create_chat

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_config', methods=['GET'])
def get_config():
    return get_conf_data(), 200
    

@app.route('/set_config', methods=['GET', 'POST'])
def set_config():
    handler = request.json.get('handler')
    name = request.json.get('name')
    value = request.json.get('value')
    logging.info('set_config -> handler: %s name: %s, value: %s' % (handler, name, value))
    if(handler.strip() == ''):
        return 'the handler is None', 400

    if(name.strip() == ''):
        return 'the name is None', 400

    if str(value).strip() == '':
        return 'the value is None', 400

    set_conf_data(handler, name, value)
    
    return 'ok', 200

@app.route('/chat_status', methods=['GET'])
def chat_status():
    chat_therad = get_chat_thread()
    msg_lock.acquire()
    msg = get_msg()
    msg_lock.release()
    if chat_therad is None or not chat_therad.is_alive():
        return {'status': 1, 'msg' : msg}, 200
    return {'status': 0, 'msg': msg}, 200


@app.route('/stop_chat', methods=['GET'])
def stop_chat():
    stop_chat_thread()
    return 'ok', 200

@app.route('/start_chat', methods=['GET'])
def start_chat():
    create_chat()
    return 'ok', 200


def create_app():
    app.run(host='0.0.0.0', port=5000)

    # return flask_app