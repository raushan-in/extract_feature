"""
Factory for creating LLM clients.
"""

import logging
from typing import List, Optional

from .base import BaseLLMClient
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient
from .groq_client import GroqClient

logger = logging.getLogger(__name__)


def create_llm_client(
    provider: str,
    api_key: str,
    model: Optional[str],
    features_list: List[str]
) -> BaseLLMClient:
    """
    Factory function to create the appropriate LLM client.
    
    Args:
        provider: LLM provider name (openai, anthropic, groq)
        api_key: API key for the provider
        model: Model name (or None to use default)
        features_list: List of features to extract
        
    Returns:
        Initialized LLM client
        
    Raises:
        ValueError: If the provider is not supported
    """
    provider = provider.lower()
    
    llm_clients = {
        'openai': {
            'class': OpenAIClient,
            'default_model': "gpt-4o"
        },
        'anthropic': {
            'class': AnthropicClient,
            'default_model': "claude-3-5-sonnet-20240620"
        },
        'groq': {
            'class': GroqClient,
            'default_model': "llama3-70b-8192"
        }
    }
    
    if provider not in llm_clients:
        logger.error(f"Unsupported LLM provider: {provider}")
        raise ValueError(f"Unsupported LLM provider: {provider}. Supported providers: {list(llm_clients.keys())}")
    
    client_info = llm_clients[provider]
    logger.info(f"Creating {provider} client with model {model or client_info['default_model']}")
    
    try:
        return client_info['class'](
            api_key, 
            model or client_info['default_model'],
            features_list
        )
    except Exception as e:
        logger.error(f"Failed to create {provider} client: {str(e)}")
        raise
