'''
Author: MeowKJ
Date: 2023-02-02 14:41:56
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-03 00:29:16
FilePath: /ChatMeow/meow/web/app.py
'''
from flask import Flask, render_template
from flask import request
# from flask_cors import CORS

import logging

from meow.utils.conf import get_conf_data
from meow.utils.conf import set_conf_data


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
    print(type(value))
    if(handler.strip() == ''):
        return 'the handler is None', 400

    if(name.strip() == ''):
        return 'the name is None', 400

    if str(value).strip() == '':
        return 'the value is None', 400

    set_conf_data(handler, name, value)
    
    return 'ok', 200


def create_app():
    logging.debug('Start create FLASK app')
    # CORS(app, resources=r'/*')
    app.run(host='0.0.0.0', port=5000)

    # return flask_app