'''
Author: MeowKJ
Date: 2023-01-25 18:32:01
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 23:17:29
FilePath: /ChatMeow/meow/ai/openai_api.py
'''
import openai
from meow.utils.context import get_db_manager
from meow.utils.retry import network_retry
import logging

# def prompt_filter(prompt):
#     return prompt != '' and prompt != 'Bot:' and prompt != 'Me:'


class ChatMeow(object):
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
            logging.error('OPENAI CHAT GET EMPTY')
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
            logging.error('OPENAI NETWORK ERROR. errror msg "{}"'.str(e))
            return 1, 'retry'

        get_db_manager().add_one_prompt("Me", new_prompt.replace('\n', ''))
        get_db_manager().add_one_prompt("Bot", text.replace('\n', ''))

        return 0, text


# def save_prompt(prompt, max_prompt_length, prompt_path):
#     prompt_list = prompt.split('\n')
#     new_prompt_list = list(filter(prompt_filter, prompt_list))
#     if (len("".join(new_prompt_list)) > max_prompt_length):
#         while (len("".join(new_prompt_list)) > max_prompt_length):
#             print("max_prompt_length", max_prompt_length)
#             del new_prompt_list[2]
#         '\n'.join(new_prompt_list)
#     try:
#         with open(prompt_path, 'w', encoding='utf-8') as f:
#             f.write("\n".join(new_prompt_list))
#     except Exception as e:
#         print(e)
