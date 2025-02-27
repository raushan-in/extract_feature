"""
Configuration management for the feature extraction system.
Handles loading and validating configuration from environment variables and config files.
"""

import os
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "llm": {
        "provider": "groq",
        "model": None
    },
    "paths": {
        "features": "features.txt",
        "input_dir": "input_files",
        "output_dir": "output_files",
        "processed_dir": "processed_files",
        "file_pattern": "product_*.txt"
    },
    "processing": {
        "batch_size": 5
    }
}


class ConfigManager:
    """
    Manages configuration for the feature extraction system.
    Handles loading from environment variables and YAML files.
    """

    def __init__(self, config_path: str = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to a YAML configuration file
        """
        self.config = {}
        self._load_default_config()
        self._load_env_vars()
        
        if config_path:
            self._load_yaml_config(config_path)
            
        self._validate_config()
        
    def _load_default_config(self) -> None:
        """Load the default configuration."""
        self.config = DEFAULT_CONFIG.copy()
        logger.debug("Loaded default configuration")
        
    def _load_env_vars(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "LLM_PROVIDER": ("llm", "provider"),
            "LLM_MODEL": ("llm", "model"),
            "FEATURES_FILE": ("paths", "features"),
            "INPUT_DIR": ("paths", "input_dir"),
            "OUTPUT_DIR": ("paths", "output_dir"),
            "PROCESSED_DIR": ("paths", "processed_dir"),
            "FILE_PATTERN": ("paths", "file_pattern"),
            "BATCH_SIZE": ("processing", "batch_size")
        }
        
        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var].strip()
                
                # Convert value to appropriate type
                if config_path[0] == "processing" and config_path[1] == "batch_size":
                    try:
                        value = int(value)
                    except ValueError:
                        logger.warning(f"Invalid value for {env_var}: {value}. Using default.")
                        continue
                
                # Update config
                section, key = config_path
                if section not in self.config:
                    self.config[section] = {}
                self.config[section][key] = value
                logger.debug(f"Set {section}.{key} from environment variable {env_var}")
                
    def _load_yaml_config(self, config_path: str) -> None:
        """
        Load configuration from a YAML file.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)
                
            if not yaml_config:
                logger.warning(f"Config file {config_path} is empty or invalid")
                return
                
            # Update configuration with YAML values
            for section, values in yaml_config.items():
                if section not in self.config:
                    self.config[section] = {}
                    
                if isinstance(values, dict):
                    for key, value in values.items():
                        self.config[section][key] = value
                        logger.debug(f"Set {section}.{key} from YAML configuration")
                else:
                    logger.warning(f"Invalid section in YAML config: {section}")
                    
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.error(f"Error loading config from {config_path}: {str(e)}")
            logger.warning("Using default/environment configuration instead")
    
    def _validate_config(self) -> None:
        """Validate the configuration and fix any issues."""
        # Validate LLM provider
        valid_providers = ["openai", "anthropic", "groq"]
        if self.config["llm"]["provider"].lower() not in valid_providers:
            logger.warning(f"Invalid LLM provider: {self.config['llm']['provider']}. Using default: groq")
            self.config["llm"]["provider"] = "groq"
            
        # Validate batch size
        if not isinstance(self.config["processing"]["batch_size"], int) or self.config["processing"]["batch_size"] < 1:
            logger.warning(f"Invalid batch size: {self.config['processing']['batch_size']}. Using default: 5")
            self.config["processing"]["batch_size"] = 5
    
    def get_api_key(self) -> str:
        """
        Get the API key for the configured LLM provider.
        
        Returns:
            The API key from environment variables
            
        Raises:
            ValueError: If the API key is not found
        """
        provider = self.config["llm"]["provider"].upper()
        env_var_name = f"{provider}_API_KEY"
        
        api_key = os.environ.get(env_var_name)
        
        if not api_key:
            logger.error(f"{env_var_name} environment variable not found")
            raise ValueError(f"API key not found. Please set {env_var_name} environment variable.")
        
        return api_key
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the complete configuration.
        
        Returns:
            The complete configuration dictionary
        """
        return self.config
