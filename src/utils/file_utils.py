"""
File utility functions for the feature extraction system.
"""

import os
import shutil
import logging
import pandas as pd
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def load_features(features_file: str) -> List[str]:
    """
    Load features from a text file.
    
    Args:
        features_file: Path to the features file
        
    Returns:
        List of feature names
        
    Raises:
        ValueError: If no features are found
    """
    try:
        with open(features_file, 'r', encoding='utf-8') as f:
            features = [line.strip() for line in f if line.strip()]
        
        if not features:
            logger.error(f"No features found in {features_file}")
            raise ValueError(f"Features file {features_file} is empty")
            
        logger.info(f"Loaded {len(features)} features from {features_file}")
        return features
    except FileNotFoundError:
        logger.error(f"Features file not found: {features_file}")
        raise
    except Exception as e:
        logger.error(f"Failed to load features from {features_file}: {str(e)}")
        raise


def load_product_description(product_file: str) -> str:
    """
    Load product description from file.
    
    Args:
        product_file: Path to the product description file
        
    Returns:
        Product description text
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(product_file, 'r', encoding='utf-8') as f:
            product_text = f.read()
        
        if not product_text.strip():
            logger.warning(f"Product file {product_file} is empty")
            
        return product_text
    except UnicodeDecodeError:
        logger.error(f"Failed to decode {product_file} as UTF-8, trying with other encodings")
        # Try alternative encodings
        for encoding in ['latin1', 'cp1252', 'iso-8859-1']:
            try:
                with open(product_file, 'r', encoding=encoding) as f:
                    product_text = f.read()
                logger.info(f"Successfully decoded {product_file} using {encoding}")
                return product_text
            except UnicodeDecodeError:
                continue
                
        # If we get here, all encodings failed
        logger.error(f"Failed to decode {product_file} with any encoding")
        raise
    except Exception as e:
        logger.error(f"Failed to read product file {product_file}: {str(e)}")
        raise


def write_to_excel(product_name: str, features: Dict[str, Any], output_dir: str) -> str:
    """
    Write extracted features to Excel file.
    
    Args:
        product_name: Name of the product file
        features: Dictionary of extracted features
        output_dir: Directory to write the output file
        
    Returns:
        Path to the created Excel file
        
    Raises:
        IOError: If the file cannot be written
    """
    try:
        df = pd.DataFrame(list(features.items()), columns=['Feature', 'Value'])
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.debug(f"Created output directory: {output_dir}")
            
        # Generate output filename
        product_id = os.path.splitext(os.path.basename(product_name))[0]
        output_file = os.path.join(output_dir, f"{product_id}.xlsx")
        
        df.to_excel(output_file, index=False)
        logger.info(f"Saved extracted features to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to write Excel file for {product_name}: {str(e)}")
        raise


def move_to_processed(file_path: str, processed_dir: str, error: bool = False) -> str:
    """
    Move processed file to the processed directory.
    
    Args:
        file_path: Path to the file to move
        processed_dir: Directory to move the file to
        error: Whether the file had processing errors
        
    Returns:
        Path to the moved file
        
    Raises:
        IOError: If the file cannot be moved
    """
    try:
        # Create processed directory if it doesn't exist
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
            logger.debug(f"Created processed directory: {processed_dir}")
        
        # If error occurred, move to error subfolder
        if error:
            error_dir = os.path.join(processed_dir, "errors")
            if not os.path.exists(error_dir):
                os.makedirs(error_dir)
                logger.debug(f"Created error directory: {error_dir}")
            destination = os.path.join(error_dir, os.path.basename(file_path))
        else:
            destination = os.path.join(processed_dir, os.path.basename(file_path))
        
        # Move the file
        shutil.move(file_path, destination)
        
        if error:
            logger.warning(f"Moved file with errors to {destination}")
        else:
            logger.info(f"Moved processed file to {destination}")
        
        return destination
    except Exception as e:
        logger.error(f"Failed to move file {file_path}: {str(e)}")
        raise


def ensure_directories(directories: List[str]) -> None:
    """
    Ensure all specified directories exist.
    
    Args:
        directories: List of directory paths to create if they don't exist
        
    Raises:
        IOError: If a directory cannot be created
    """
    for directory in directories:
        try:
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.debug(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {str(e)}")
            raise