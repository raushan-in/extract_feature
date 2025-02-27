"""
Groq API client implementation.
"""

import logging
from typing import List

from langchain_groq import ChatGroq

from .base import BaseLLMClient

logger = logging.getLogger(__name__)


class GroqClient(BaseLLMClient):
    """
    Groq API client for feature extraction.
    """
    
    def __init__(self, api_key: str, model_name: str = "llama3-70b-8192", features_list: List[str] = None):
        """
        Initialize the Groq client.
        
        Args:
            api_key: Groq API key
            model_name: Name of the model to use (default: llama3-70b-8192)
            features_list: List of features to extract
        """
        super().__init__(api_key, model_name, features_list)
        try:
            self.llm = ChatGroq(
                api_key=api_key,
                model=model_name,
                temperature=0.1,
                timeout=60
            )
            logger.info(f"Initialized Groq client with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise
