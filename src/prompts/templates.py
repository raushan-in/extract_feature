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
        I have a product description and need to extract specific features accurately.
        
        PRODUCT DESCRIPTION:
        {product_text}
        
        FEATURES TO EXTRACT:
        {features_list}
        
        TASK:
        1. Extract the values for as many features as possible from the product description
        2. Return only values that are explicitly stated or can be directly inferred
        3. For numerical values, extract only the number without units (normalize)
        4. For dimensions (height, width, depth), extract only the number in mm
        5. If a feature is not found, set its value to null
        6. For boolean features (with "With" or "Suitable for"), use true/false
        
        {format_instructions}
        """,
        input_variables=["product_text", "features_list"],
        partial_variables={"format_instructions": format_instructions}
    )