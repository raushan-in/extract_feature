"""
Base class for LLM clients.
"""

import logging
import time
from typing import Dict, List, Any

from langchain.output_parsers import PydanticOutputParser

from ..models.feature_model import ExtractedFeatures
from ..prompts.templates import get_feature_extraction_prompt

logger = logging.getLogger(__name__)


class BaseLLMClient:
    """
    Base class for all LLM API clients.
    """
    
    def __init__(self, api_key: str, model_name: str, features_list: List[str]):
        """
        Initialize the LLM client.
        
        Args:
            api_key: API key for the LLM service
            model_name: Name of the model to use
            features_list: List of features to extract
        """
        self.api_key = api_key
        self.model_name = model_name
        self.features_list = features_list
        self.feature_model = ExtractedFeatures.create_model_class(features_list)
        self.parser = PydanticOutputParser(pydantic_object=self.feature_model)
        self.llm = None
        self._setup_prompt_template()
        
    def _setup_prompt_template(self):
        """
        Set up the prompt template with format instructions.
        """
        self.prompt_template = get_feature_extraction_prompt(self.parser.get_format_instructions())

    def extract_features(self, product_text: str) -> Dict[str, Any]:
        """
        Extract features from product text using the LLM.
        
        Args:
            product_text: Text description of the product
            
        Returns:
            Dictionary of extracted features
            
        Raises:
            ValueError: If the LLM client is not initialized
        """
        if not self.llm:
            logger.error("LLM client not initialized")
            raise ValueError("LLM client not initialized")
            
        try:
            formatted_features = "\n".join([f"- {feature}" for feature in self.features_list])
            prompt_value = self.prompt_template.format(
                product_text=product_text,
                features_list=formatted_features
            )
            
            # Add retry logic
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    result = self.llm.invoke(prompt_value)
                    parsed_result = self.parser.parse(result)
                    logger.debug(f"Successfully extracted features on attempt {attempt+1}")
                    return parsed_result
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"LLM processing failed, retrying in {retry_delay}s: {str(e)}")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        logger.error(f"LLM processing failed after {max_retries} attempts: {str(e)}")
                        raise
                        
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            # Return empty features as fallback
            return {feature: None for feature in self.features_list}
