"""
Prompt templates for feature extraction.
"""

from langchain_core.prompts import PromptTemplate


def get_feature_extraction_prompt() -> PromptTemplate:
    """
    Creates a prompt template for extracting features from product descriptions.

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
        - Extract only numbers without units (e.g. 5 instead of 5 mm, 26.3 instead of 26.3 kW)
        - Ensure that the extracted values are normalized (e.g. "5/3 mm" should be "1.67")
        - For boolean features use true/false
        - Don't guess values that aren't directly stated or clearly implied
        - If a feature has a range (e.g., "5-10 kW"), extract the maximum value (10)
        - Format percentage values as decimals (0.25 instead of 25%)

        Return format: {{ "feature1": value1, "feature2": value2, ... }}
        """,
        input_variables=["product_text", "features_list"],
    )
