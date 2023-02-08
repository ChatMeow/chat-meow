'''
Author: MeowKJ
Date: 2023-02-02 16:05:00
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-08 15:11:03
FilePath: /chat-meow/meow/utils/retry.py
'''
from functools import wraps
import time
import logging
from meow.utils.context import context

def network_retry(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        code, text = f(*args, **kwargs)
        while code == 1:
            logging.info('Wait {}s before retry, current retries [{}] , max retries [{}]'.format(context['retry.timewait'],
                                                                                                 context['retry.current_retries'], context['retry.max_retries']))
            time.sleep(context['retry.timewait'])
            code, text = f(*args, **kwargs)
            context['retry.current_retries'] = context['retry.current_retries'] + 1
            if context['retry.current_retries'] > context['retry.max_retries']:
                raise Exception('Max retries exceeded')
        context['retry.current_retries'] = 1
        return code, text
    return decorated


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logging.debug(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging
