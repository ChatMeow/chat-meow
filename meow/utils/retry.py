from functools import wraps
import time
import logging
from meow.utils.context import context


def network_retry(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        code, text = f(*args, **kwargs)
        while code == 1:
            logging.warning('Wait {}s before retry, current retries [{}] , max retries [{}]'
                         .format(context.retry_delay, context.current_retries, context.max_retries))
            time.sleep(context.retry_delay)
            code, text = f(*args, **kwargs)
            context.current_retries = context.current_retries + 1
            if context.current_retries > context.max_retries:
                raise Exception('Max retries exceeded')
        context.current_retries = 1
        return code, text

    return decorated


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logging.debug(func.__name__ + " was called")
        return func(*args, **kwargs)

    return with_logging
