"""
Pydantic models for feature extraction.
"""

import re
import json
import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ExtractedFeatures:
    """
    Factory for dynamic feature models based on feature lists.
    """

    @classmethod
    def create_model_class(cls, features_list: List[str]) -> type:
        """
        Create a dynamic model class based on a list of features.

        Args:
            features_list: List of feature names to include in the model

        Returns:
            A dynamically generated Pydantic model class
        """
        try:
            # Create field definitions for each feature
            annotations = {feature: Optional[Any] for feature in features_list}
            attributes = {
                feature: Field(default=None, description=f"Value for {feature}")
                for feature in features_list
            }

            # Create a new model class dynamically
            return type(
                "DynamicFeatureModel",
                (BaseModel,),
                {"__annotations__": annotations, **attributes},
            )
        except Exception as e:
            logger.error(f"Failed to create dynamic feature model: {str(e)}")
            raise


def normalize_features(
    extracted: Dict[str, Any], features_list: List[str]
) -> Dict[str, Any]:
    """
    Post-process and normalize extracted features.

    Args:
        extracted: Raw extracted features dictionary
        features_list: List of expected features

    Returns:
        Normalized features dictionary with consistent types
    """

    normalized = {feature: None for feature in features_list}

    for feature, value in extracted.items():
        if feature not in features_list:
            continue

        if value is None:
            normalized[feature] = None
            continue

        # Convert string numbers to actual numbers
        if isinstance(value, str) and re.match(r"^-?\d+(\.\d+)?$", value.strip()):
            try:
                if "." in value:
                    normalized[feature] = float(value)
                else:
                    normalized[feature] = int(value)
            except:
                normalized[feature] = value
        # Convert boolean string representations to actual booleans
        elif isinstance(value, str) and value.lower() in ["true", "false"]:
            normalized[feature] = value.lower() == "true"
        else:
            normalized[feature] = value

    return normalized


def parse_and_normalize_response(response_text: str, features_list: List[str]) -> Dict[str, Any]:
    """
    Parse JSON from LLM response and normalize values in a single pass.
    
    Args:
        response_text: Raw text response from LLM
        features_list: List of expected features
        
    Returns:
        Normalized features dictionary with consistent types
    """
    # Initialize result dictionary with None values
    normalized = {feature: None for feature in features_list}
    
    try:
        # Extract JSON from potential text wrapping (supports multi-line JSON)
        json_match = re.search(r'{.*}', response_text, re.DOTALL)
        if not json_match:
            logger.warning("No JSON object found in response")
            return normalized

        json_str = json_match.group(0)
        extracted_data = json.loads(json_str)
        
        for feature in features_list:
            if feature not in extracted_data:
                continue
                
            value = extracted_data[feature]
            if value is None:
                continue
                
            # Convert string numbers to actual numbers
            if isinstance(value, str) and re.match(r"^-?\d+(\.\d+)?$", value.strip()):
                try:
                    normalized[feature] = float(value) if "." in value else int(value)
                except:
                    normalized[feature] = value
            # Convert boolean string representations to actual booleans
            elif isinstance(value, str) and value.lower() in ["true", "false"]:
                normalized[feature] = value.lower() == "true"
            else:
                normalized[feature] = value
                
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")
        
    return normalized