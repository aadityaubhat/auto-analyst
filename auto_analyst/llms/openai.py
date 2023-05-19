from auto_analyst.llms.base import BaseLLM
import openai
import enum
import re


class Model(enum.Enum):
    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"


class OpenAILLM(BaseLLM):
    """Class for OpenAI LLM"""

    def __init__(
        self,
        api_key: str,
        model: Model,
        temperature: float = 0.2,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
    ):
        """Initialize OpenAI LLM"""
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        openai.api_key = self.api_key

    def get_reply(self, prompt=None, system_prompt=None, messages: list = []):
        if not prompt and not system_prompt and not messages:
            raise ValueError(
                "Please provide either messages or prompt and system_prompt"
            )
        elif not messages:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]

        response = openai.ChatCompletion.create(
            model=self.model.value,
            messages=messages,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
        )

        return response["choices"][0]["message"]["content"].strip()

    def get_code(self, prompt=None, system_prompt=None, messages: list = []):
        reply = self.get_reply(prompt, system_prompt, messages)
        pattern = r"```(.*?)```"
        matches = re.findall(pattern, reply, re.DOTALL)

        if matches:
            code = matches[0].strip()
            return code
        else:
            raise ValueError(f"No code found in the reply: \n{reply}")
