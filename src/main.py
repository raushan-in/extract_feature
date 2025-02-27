"""
Main entry point for the feature extraction application.
"""

import argparse
import sys

from dotenv import load_dotenv

from .config.config_manager import ConfigManager
from .llm.factory import create_llm_client
from .processors.batch_processor import BatchProcessor
from .utils.file_utils import load_features
from .utils.logging import get_console_level, setup_logging


def main():
    """
    Main entry point for the feature extraction application.
    """
    try:
        load_dotenv(override=True)
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Extract features from product descriptions using LLMs"
    )
    parser.add_argument(
        "--config", type=str, help="Path to configuration file (optional)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress console output except errors",
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging(console_level=get_console_level(args.verbose, args.quiet))

    try:
        # Load configuration
        config_manager = ConfigManager(args.config)
        config = config_manager.get_config()

        # Get API key
        provider = config["llm"]["provider"]
        api_key = config_manager.get_api_key()

        # Load features
        features_list = load_features(config["paths"]["features"])

        # Create LLM client
        client = create_llm_client(
            provider, api_key, config["llm"]["model"], features_list
        )

        # Process files in batches
        logger.info("Starting batch processing")
        processor = BatchProcessor(client, config)
        results = processor.process_files()

        # Show summary
        logger.info(f"Feature extraction completed!")
        logger.info(f"Total files: {results['total_files']}")
        logger.info(
            f"Successfully processed: {results['success_count']} ({results['success_rate']:.1%})"
        )
        logger.info(f"Errors: {results['error_count']}")

        return 0

    except Exception as e:
        logger.error(f"🛑: {e}")
        return 1


if __name__ == "__main__":
    # Run with proper exit code for potential CI/CD integration
    sys.exit(main())
