import openai
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from meow.utils.context import context
from meow.utils.retry import network_retry
import logging



# def prompt_filter(prompt):
#     return prompt != '' and prompt != 'Bot:' and prompt != 'Me:'

class OneapiHandler(object):
    def __init__(self, api_key, api, max_prompt_length, default_prompt, ai_params=None):
        if ai_params is None:
            ai_params = {}
        self.oneapi = OpenAI(api_key=api_key, base_url=api)
        self.ai_params = ai_params
        self.max_prompt_length = max_prompt_length
        self.default_prompt = {"role": "system", "content": default_prompt}

    @network_retry
    def chat(self, content: str) -> tuple[int, str]:
        # ? 检查prompt格式
        if content == '' or content == ' ':
            logging.warning('ONEAPI CHAT GET EMPTY')
            return 2, 'restart'
        # ? 用于openai的prompt格式
        new_prompt = {"role": "user", "content": content}
        # ? 载入之前的prompt, 如果为空则新建
        try:
            prompt_list = context.get_db_manager().get_prompt(self.max_prompt_length)
            prompt_list.append(new_prompt)
        except Exception as e:
            prompt_list = [new_prompt]
            logging.warning(
                f'Database get prompt error {str(e)}. let prompt same with new prompt {new_prompt}')
        # ? 加入初始prompt
        prompt = [self.default_prompt] + prompt_list
        logging.debug('OPENAI NETWORK START, prompt: {}'.format(prompt))

        try:
            response = self.oneapi.chat.completions.create(
                messages=prompt,
                timeout=5,
                stream=False,
                **self.ai_params
            )
            logging.debug('OPENAI NETWORK SUCCESS, response: {}'.format(response.dict()))
            text: str = response.dict()['choices'][0]['message']['content']
            if text.strip() == '':
                logging.error(
                    'BOT SAY NOTHING -> the bot return the "{}"'.format(text))
                return 2, 'restart'

        except Exception as e:
            logging.error('OPENAI NETWORK ERROR. error msg "{}"'.format(str(e)))
            return 1, 'retry'

        context.get_db_manager().add_one_prompt("user", new_prompt["content"])
        context.get_db_manager().add_one_prompt("assistant", text)

        return 0, text
