import unittest
from unittest.mock import patch

from src.config.config_manager import ConfigManager
from src.utils.parser import parse_and_normalize_response
from src.prompts.templates import get_feature_extraction_prompt


class FeatureExtractionTests(unittest.TestCase):

    def setUp(self):
        self.test_features = ["brand", "model", "power"]

    def test_config_manager_loads_defaults(self):
        """Test that ConfigManager properly loads default configuration."""
        config_manager = ConfigManager()
        config = config_manager.get_config()

        # Check default values
        self.assertEqual(config["llm"]["provider"], "groq")
        self.assertEqual(config["paths"]["features"], "features/features.txt")
        self.assertEqual(config["processing"]["batch_size"], 5)

    @patch("os.environ", {"LLM_PROVIDER": "anthropic"})
    def test_config_manager_loads_env_vars(self):
        """Test that ConfigManager properly loads environment variables."""
        with patch("os.environ", {"LLM_PROVIDER": "anthropic"}):
            config_manager = ConfigManager()
            config = config_manager.get_config()

            # Check value from environment variable
            self.assertEqual(config["llm"]["provider"], "anthropic")

    def test_feature_extraction_prompt(self):
        """Test that the prompt template is generated correctly."""
        prompt_template = get_feature_extraction_prompt()

        rendered_prompt = prompt_template.format(
            product_text="This is a test product.", features_list="brand, model"
        )

        # Check that key elements are in the prompt
        self.assertIn("This is a test product.", rendered_prompt)
        self.assertIn("brand, model", rendered_prompt)

    def test_parse_and_normalize_response(self):
        """Test that response parsing and normalization works correctly."""
        # Sample LLM response with JSON
        response_text = """
        Here's what I found:
        
        {
            "brand": "TestBrand",
            "model": "XYZ-123",
            "power": "100.5",
            "unknown_feature": "value"
        }
        """

        result = parse_and_normalize_response(response_text, self.test_features)

        # Check extraction results
        self.assertEqual(result["brand"], "TestBrand")
        self.assertEqual(result["model"], "XYZ-123")
        self.assertEqual(result["power"], 100.5)  # Should convert to float
        self.assertNotIn("unknown_feature", result)  # Should ignore unexpected features


if __name__ == "__main__":
    unittest.main()
