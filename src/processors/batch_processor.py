"""
Batch processing for multiple product files.
"""

import glob
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict

from tqdm import tqdm

from ..llm.base import BaseLLMClient
from ..utils.file_utils import ensure_directories
from .extractor import FeatureExtractor

logger = logging.getLogger(__name__)


class BatchProcessor:
    """
    Process multiple product files in batches.
    """

    def __init__(self, client: BaseLLMClient, config: Dict):
        """
        Initialize the batch processor.

        Args:
            client: LLM client to use for extraction
            config: Configuration dictionary
        """
        self.client = client
        self.config = config
        self.input_dir = config["paths"]["input_dir"]
        self.output_dir = config["paths"]["output_dir"]
        self.processed_dir = config["paths"]["processed_dir"]
        self.file_pattern = config["paths"]["file_pattern"]
        self.batch_size = config["processing"]["batch_size"]

        # Create extractor for individual files
        self.extractor = FeatureExtractor(client, self.output_dir, self.processed_dir)

    def process_files(self) -> Dict:
        """
        Process all product files matching the pattern in the input directory.

        Returns:
            Dictionary with processing results and statistics
        """
        # Ensure all required directories exist
        ensure_directories([self.input_dir, self.output_dir, self.processed_dir])

        # Get all product files matching the pattern
        try:
            product_files = glob.glob(os.path.join(self.input_dir, self.file_pattern))
        except Exception as e:
            logger.error(
                f"Failed to find files matching pattern {self.file_pattern}: {str(e)}"
            )
            raise

        if not product_files:
            logger.warning(
                f"No files matching {self.file_pattern} found in {self.input_dir}"
            )
            return {
                "total_files": 0,
                "processed_files": 0,
                "success_count": 0,
                "error_count": 0,
                "success_rate": 0,
                "files": [],
            }

        total_files = len(product_files)
        logger.info(f"Found {total_files} files to process")

        # Process files in parallel with progress bar
        results = []
        with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
            futures = {}

            # Submit all tasks
            for product_file in product_files:
                future = executor.submit(self.extractor.process_file, product_file)
                futures[future] = product_file

            # Process with progress bar
            with tqdm(
                total=len(futures), desc="Processing files", unit="file"
            ) as progress_bar:
                for future in as_completed(futures):
                    file_path = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.error(
                            f"Unexpected error processing {os.path.basename(file_path)}: {str(e)}"
                        )
                        results.append(
                            {
                                "file": os.path.basename(file_path),
                                "success": False,
                                "features_found": 0,
                                "error": str(e),
                            }
                        )
                    progress_bar.update(1)

        # Calculate summary statistics
        success_count = sum(1 for r in results if r["success"])
        error_count = len(results) - success_count
        success_rate = success_count / len(results) if results else 0
        logger.info(
            f"Processing complete: {success_count}/{len(results)} files successful ({success_rate:.1%})"
        )

        summary = {
            "total_files": total_files,
            "processed_files": len(results),
            "success_count": success_count,
            "error_count": error_count,
            "success_rate": success_rate,
            "files": results,
        }

        # Save summary to file
        try:
            with open("extraction_summary.json", "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
            logger.info("Wrote processing summary to extraction_summary.json")
        except Exception as e:
            logger.warning(f"Failed to write summary report: {str(e)}")

        return summary
