"""
Pydantic models for feature extraction.
"""

from typing import Any, Dict, List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field


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
        # Create field definitions for each feature
        fields = {
            feature: (Optional[Any], Field(description=f"Value for {feature}", default=None)) 
            for feature in features_list
        }
        
        # Create a new model class dynamically
        return type('DynamicFeatureModel', (BaseModel,), {
            '__annotations__': fields,
            **fields
        })


def normalize_features(
    extracted: Dict[str, Any], 
    features_list: List[str]
) -> Dict[str, Any]:
    """
    Post-process and normalize extracted features.
    
    Args:
        extracted: Raw extracted features dictionary
        features_list: List of expected features
        
    Returns:
        Normalized features dictionary with consistent types
    """
    import re
    
    normalized = {feature: None for feature in features_list}
    
    for feature, value in extracted.items():
        if feature not in features_list:
            continue
            
        if value is None:
            normalized[feature] = None
            continue
            
        # Convert string numbers to actual numbers
        if isinstance(value, str) and re.match(r'^-?\d+(\.\d+)?$', value.strip()):
            try:
                if '.' in value:
                    normalized[feature] = float(value)
                else:
                    normalized[feature] = int(value)
            except:
                normalized[feature] = value
        # Convert boolean string representations to actual booleans
        elif isinstance(value, str) and value.lower() in ['true', 'false']:
            normalized[feature] = value.lower() == 'true'
        else:
            normalized[feature] = value
    
    return normalized
