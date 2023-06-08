from auto_analyst.llms.base import BaseLLM
import openai
import enum
import re
import logging
from typing import (
    Optional,
    List,
    Dict,
)

logger = logging.getLogger(__name__)


class Model(enum.Enum):
    """Enum for OpenAI LLM Models"""

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"


class OpenAILLM(BaseLLM):
    """Class for OpenAI LLM
    Attributes:
        api_key (str): OpenAI API Key
        model (Model): OpenAI LLM Model
        temperature (float): Temperature for generating reply
        frequency_penalty (float): Frequency penalty for generating reply
        presence_penalty (float): Presence penalty for generating reply"""

    def __init__(
        self,
        api_key: str,
        model: Model,
        temperature: float = 0.2,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
    ):
        """Initialize OpenAI LLM
        Args:
            api_key (str): OpenAI API Key
            model (Model): OpenAI LLM Model
            temperature (float): Temperature for generating reply
            frequency_penalty (float): Frequency penalty for generating reply
            presence_penalty (float): Presence penalty for generating reply
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        openai.api_key = self.api_key

    def get_reply(
        self,
        prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        messages: List[Dict[str, str]] = [],
        **kwargs,
    ) -> str:
        """Get reply from OpenAI LLM
        Args:
            prompt (Optional[str]): Prompt to be used for generating reply
            system_prompt (Optional[str]): System prompt to be used for generating reply
            messages (List[Dict[str, str]]): List of messages to be used for generating reply
        Returns:
            str: Reply from OpenAI LLM"""
        if not prompt and not system_prompt and not messages:
            raise ValueError(
                "Please provide either messages or prompt and system_prompt"
            )
        elif not messages:
            messages = [
                {"role": "system", "content": system_prompt},  # type: ignore[dict-item]
                {"role": "user", "content": prompt},  # type: ignore[dict-item]
            ]

        logger.info(f"Messages: {messages}")
        try:
            response = openai.ChatCompletion.create(
                model=self.model.value,
                messages=messages,
                temperature=self.temperature,
                frequency_penalty=self.frequency_penalty,
            )
            logger.info(f"Response: {response}")
        except openai.error.APIConnectionError as e:
            # Handle connection error here
            logger.error(f"Failed to connect to OpenAI API: {e}")
            raise Exception(f"Failed to connect to OpenAI API: {e}")
        except openai.error.APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise Exception(f"OpenAI API Error: {e}")
        except openai.error.RateLimitError as e:
            logger.error(f"OpenAI API Rate Limit Error: {e}")
            raise Exception(f"OpenAI API Rate Limit Error: {e}")
        except openai.error.AuthenticationError as e:
            logger.error(
                f"OpenAI API Authentication Error:{e}\nCheck your OpenAI API key in config.json"
            )
            raise Exception(
                f"OpenAI API Authentication Error:{e}\nCheck your OpenAI API key in config.json"
            )
        except openai.error.InvalidRequestError as e:
            logger.error(f"OpenAI API Invalid Request Error: {e}")
            raise Exception(f"OpenAI API Invalid Request Error: {e}")
        return response["choices"][0]["message"]["content"].strip()

    async def get_reply_async(
        self, prompt=None, system_prompt=None, messages: list = []
    ):
        if not prompt and not system_prompt and not messages:
            raise ValueError(
                "Please provide either messages or prompt and system_prompt"
            )
        elif not messages:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        logger.info(f"Messages: {messages}")
        response = await openai.ChatCompletion.create(
            model=self.model.value,
            messages=messages,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
        )
        logger.info(f"Response: {response}")

        return response["choices"][0]["message"]["content"].strip()

    def get_code(
        self,
        prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        messages: List[Dict[str, str]] = [],
        **kwargs,
    ) -> str:
        """Get code from OpenAI LLM reply
        Args:
            prompt (Optional[str]): Prompt to be used for generating reply
            system_prompt (Optional[str]): System prompt to be used for generating reply
            messages (List[Dict[str, str]]): List of messages to be used for generating reply
        Returns:
            str: Code from OpenAI LLM reply"""
        reply = self.get_reply(prompt, system_prompt, messages)
        pattern = r"```.*?\n(.*?)```"
        matches = re.findall(pattern, reply, re.DOTALL)

        if matches:
            code = matches[0].strip()
            return code
        else:
            return reply

    async def get_code_async(
        self, prompt=None, system_prompt=None, messages: list = []
    ):
        reply = await self.get_reply_async(prompt, system_prompt, messages)
        pattern = r"```.*?\n(.*?)```"
        matches = re.findall(pattern, reply, re.DOTALL)

        if matches:
            code = matches[0].strip()
            return code
        else:
            return reply
