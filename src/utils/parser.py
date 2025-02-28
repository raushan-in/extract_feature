import json
import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def parse_and_normalize_response(
    response_text: str, features_list: List[str]
) -> Dict[str, Any]:
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
        json_match = re.search(r"{.*}", response_text, re.DOTALL)
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
