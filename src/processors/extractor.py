"""
Feature extraction processor for individual product files.
"""

import logging
from typing import Dict, Any

from ..llm.base import BaseLLMClient
from ..models.feature_model import normalize_features
from ..utils.file_utils import load_product_description, write_to_excel, move_to_processed

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """
    Extracts features from product description files using an LLM.
    """
    
    def __init__(self, client: BaseLLMClient, output_dir: str, processed_dir: str):
        """
        Initialize the feature extractor.
        
        Args:
            client: LLM client to use for extraction
            output_dir: Directory to save output files
            processed_dir: Directory to move processed files
        """
        self.client = client
        self.output_dir = output_dir
        self.processed_dir = processed_dir
        
    def process_file(self, product_file: str) -> Dict[str, Any]:
        """
        Process a single product file to extract features.
        
        Args:
            product_file: Path to the product description file
            
        Returns:
            Dictionary with processing results and statistics
        """
        product_basename = product_file.split('/')[-1]
        result = {
            "file": product_basename,
            "success": False,
            "features_found": 0,
            "error": None
        }
        
        try:
            # Load product text
            logger.info(f"Processing {product_basename}")
            try:
                product_text = load_product_description(product_file)
            except Exception as e:
                logger.error(f"Failed to read product file {product_basename}: {str(e)}")
                result["error"] = f"File read error: {str(e)}"
                move_to_processed(product_file, self.processed_dir, error=True)
                return result
            
            # Extract features
            try:
                extracted_features = self.client.extract_features(product_text)
                normalized_features = normalize_features(
                    extracted_features.dict(), 
                    self.client.features_list
                )
            except Exception as e:
                logger.error(f"Feature extraction failed for {product_basename}: {str(e)}")
                result["error"] = f"Extraction error: {str(e)}"
                move_to_processed(product_file, self.processed_dir, error=True)
                return result
            
            # Calculate how many features were successfully extracted
            features_found = sum(1 for v in normalized_features.values() if v is not None)
            result["features_found"] = features_found
            
            # Save to Excel
            try:
                write_to_excel(product_basename, normalized_features, self.output_dir)
            except Exception as e:
                logger.error(f"Failed to write output file for {product_basename}: {str(e)}")
                result["error"] = f"Output write error: {str(e)}"
                move_to_processed(product_file, self.processed_dir, error=True)
                return result
            
            # Move file to processed folder
            try:
                move_to_processed(product_file, self.processed_dir)
            except Exception as e:
                logger.error(f"Failed to move {product_basename} to processed folder: {str(e)}")
                result["error"] = f"File move error: {str(e)}"
                return result
            
            logger.info(f"Successfully processed {product_basename}: {features_found}/{len(self.client.features_list)} features found")
            result["success"] = True
            
        except Exception as e:
            logger.error(f"Unexpected error processing {product_basename}: {str(e)}")
            result["error"] = f"Unexpected error: {str(e)}"
            # Still try to move the file to prevent infinite retry
            try:
                move_to_processed(product_file, self.processed_dir, error=True)
            except Exception:
                pass
            
        return result
