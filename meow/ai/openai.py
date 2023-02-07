'''
Author: MeowKJ
Date: 2023-01-25 18:32:01
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-07 17:02:25
FilePath: /chat-meow/meow/ai/openai.py
'''
import openai
from meow.utils.context import get_db_manager
from meow.utils.retry import network_retry
import logging

# def prompt_filter(prompt):
#     return prompt != '' and prompt != 'Bot:' and prompt != 'Me:'

class OpenaiHandler(object):
    def __init__(self, api_key, max_prompt_length, default_prompt_me, default_prompt_bot, openai_api_params={}):
        openai.api_key = api_key
        self.prompt_path = "prompt.txt"
        self.openai_api_params = openai_api_params
        self.max_prompt_length = max_prompt_length
        self.start_sequence = ''
        self.restart_sequence = ''
        self.default_prompt = self.restart_sequence + default_prompt_me + '\n' + self.start_sequence + default_prompt_bot
        self.current_prompt_length = 0

    @network_retry
    def chat(self, new_prompt: str) -> str:
        # ? 检查prompt格式
        if new_prompt == '' or new_prompt == ' ':
            logging.warning('OPENAI CHAT GET EMPTY')
            return 2, 'restart'

        # if new_prompt[-1] not in ['.', '。', '?', '!', '？', '！']:
        #     new_prompt = new_prompt + '.'

        # ? 给prompt装上发言人
        new_prompt = self.restart_sequence + new_prompt

        # ? 载入之前的promot, 如果为空则新建
        try:
            prompt_list = get_db_manager().get_prompt(self.max_prompt_length)
            prompt = '\n'.join(prompt_list)
            prompt = prompt + '\n' + new_prompt
        except Exception as e:
            logging.warning(
                'database get prompt error {}. let prompt same with new prompt'.format(str(e)))
            prompt = new_prompt
            return 2, 'database error'

        # ? 加入初始prompt
        prompt = self.default_prompt + prompt + '\n'
        try:
            response = openai.Completion.create(
                prompt=prompt,
                timeout=5,
                **self.openai_api_params
            )
            text: str = response.choices[0].text
            if (text.strip() == ''):
                logging.error(
                    'BOT SAY NOTHING -> the bot return the "{}"'.format(text))
                return 2, 'restart'

        except Exception as e:
            logging.error('OPENAI NETWORK ERROR. errror msg "{}"'.format(str(e)))
            return 1, 'retry'

        get_db_manager().add_one_prompt("Me", new_prompt.replace('\n', ''))
        get_db_manager().add_one_prompt("Bot", text.replace('\n', ''))

        return 0, text
