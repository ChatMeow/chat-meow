from meow.web.app import create_app
from chat import create_chat
import logging

if __name__ == '__main__':
    logging.basicConfig(
        # filename='chat.log',
        # filemode='a',
        level=logging.INFO)
    create_chat()
    create_app()


