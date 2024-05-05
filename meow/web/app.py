from flask import Flask, render_template
from flask import request

import logging

from meow.utils.conf import get_conf_data
from meow.utils.conf import set_conf_data
from meow.utils.context import context
from meow.utils.thread import stop_chat_thread

from chat import create_chat

app = Flask(__name__, static_url_path='')

# 获取Flask应用程序的日志记录器
app_logger = logging.getLogger('werkzeug')
# 设置日志级别为ERROR，即只记录ERROR级别及以上的日志
app_logger.setLevel(logging.WARNING)
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
    if handler.strip() == '':
        return 'the handler is None', 400

    if name.strip() == '':
        return 'the name is None', 400

    if str(value).strip() == '':
        return 'the value is None', 400

    set_conf_data(handler, name, value)

    return 'ok', 200


@app.route('/chat_status', methods=['GET'])
def chat_status():
    chat_thread = context.get_chat_thread()
    msg = context.get_msg()
    if chat_thread is None or not chat_thread.is_alive():
        return {'status': 1, 'msg': msg}, 200
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
