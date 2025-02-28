"""
Prompt templates for feature extraction.
"""

from langchain_core.prompts import PromptTemplate


def get_feature_extraction_prompt(format_instructions: str) -> PromptTemplate:
    """
    Creates a prompt template for extracting features from product descriptions.

    Args:
        format_instructions: Instructions for formatting the output (from output parser)

    Returns:
        A PromptTemplate object configured for feature extraction
    """
    return PromptTemplate(
        template="""
        Extract the following features from this product description. Return ONLY a valid JSON object with the feature names as keys.
        
        Product description: {product_text}
        
        Features to extract: {features_list}
        
        Rules:
        - Use null for missing values
        - Extract only numbers without units
        - For boolean features use true/false
        
        Return format: {{ "feature1": value1, "feature2": value2, ... }}
        """,
        input_variables=["product_text", "features_list"]
    )