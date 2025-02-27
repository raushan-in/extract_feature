"""
OpenAI API client implementation.
"""

import logging
from typing import List

from langchain_openai import ChatOpenAI

from .base import BaseLLMClient

logger = logging.getLogger(__name__)


class OpenAIClient(BaseLLMClient):
    """
    OpenAI API client for feature extraction.
    """

    def __init__(
        self, api_key: str, model_name: str = "gpt-4o", features_list: List[str] = None
    ):
        """
        Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key
            model_name: Name of the model to use (default: gpt-4o)
            features_list: List of features to extract
        """
        super().__init__(api_key, model_name, features_list)
        try:
            self.llm = ChatOpenAI(
                api_key=api_key, model=model_name, temperature=0.1, request_timeout=60
            )
            logger.info(f"Initialized OpenAI client with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise
