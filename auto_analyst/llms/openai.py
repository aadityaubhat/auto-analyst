from auto_analyst.llms.base import BaseLLM
import openai
import enum


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

    def get_reply(self, prompt, system_prompt, messages: list = []):
        if not messages:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        elif not prompt and not system_prompt:
            raise ValueError(
                "Please provide either messages or prompt and system_prompt"
            )

        response = openai.ChatCompletion.create(
            model=self.model.value,
            messages=messages,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
        )

        return response["choices"][0]["message"]["content"].strip()
