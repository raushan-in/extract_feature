"""
Anthropic API client implementation.
"""

import logging
from typing import List

from langchain_anthropic import ChatAnthropic

from .base import BaseLLMClient

logger = logging.getLogger(__name__)


class AnthropicClient(BaseLLMClient):
    """
    Anthropic API client for feature extraction.
    """
    
    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20240620", features_list: List[str] = None):
        """
        Initialize the Anthropic client.
        
        Args:
            api_key: Anthropic API key
            model_name: Name of the model to use (default: claude-3-5-sonnet-20240620)
            features_list: List of features to extract
        """
        super().__init__(api_key, model_name, features_list)
        try:
            self.llm = ChatAnthropic(
                api_key=api_key,
                model=model_name,
                temperature=0.1,
                max_tokens=4000,
                timeout=60
            )
            logger.info(f"Initialized Anthropic client with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise
