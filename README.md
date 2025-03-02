# Feature Extraction Tool

A tool for extracting structured features from product descriptions using LLM.

## Architecture

```
feature_extraction/
├── src/                     # Source code
│   ├── config/               # Configuration management
│   ├── llm/                 # LLM client implementations
│   ├── processors/          # Processing logic
│   ├── prompts/             # LLM prompt templates
│   ├── utils/               # Utility functions
│   └── main.py              # Entry point
```

## Setup

- `Python3.10` is required

1. Virtual Environment [Optional]

- create
```bash
python3 -m venv venv
```

 - Actvate on Windows:

```bash
venv\Scripts\activate
```

 - Actiavte on macOS/Linux:
```bash
source venv/bin/activate
```

2. Install the package: [Required]

```bash
pip install -e .
```

3. Configure your API key:

- Create `.env`
```bash
cp .env.sample .env
```

   - Uncomment and add your API key for the service you'll use

4. Add input files

- Place your product files in the input directory (default: `input_files/`)


## Start Execution  🚀
- App start

```bash
extract-features
```

### Additional Options

- Use a custom config file:
```bash
extract-features --config my_config.yaml
```

- Enable verbose logging:
```bash
extract-features --verbose
```

- Suppress console output (only show errors):
```bash
extract-features --quiet
```

## Configuration

Configure the tool using any of these methods (in order of precedence):

1. Command-line arguments
2. Environment variables in `.env` file
3. YAML configuration (optional)
4. Default values

### Configuration Options

| Setting | Env Variable | Default | Description |
|---------|--------------|---------|-------------|
| LLM Provider | `LLM_PROVIDER` | `groq` | LLM API provider (openai, anthropic, groq) |
| LLM Model | `LLM_MODEL` | *provider default* | Specific model to use |
| Features File | `FEATURES_FILE` | `features/features.txt` | Path to features definition file |
| Input Directory | `INPUT_DIR` | `input_files` | Where to find product files |
| Output Directory | `OUTPUT_DIR` | `output_files` | Where to save extracted data |
| Processed Directory | `PROCESSED_DIR` | `processed_files` | Where to move processed files |
| File Pattern | `FILE_PATTERN` | `product_*.txt` | Pattern to match input files |
| Batch Size | `BATCH_SIZE` | `5` | Number of concurrent API requests |

## Output

- **Excel Files**: Each processed product gets an Excel file with extracted features
- **Log File**: Detailed logging in `feature_extraction.log`
- **Summary Report**: JSON file with processing statistics (`extraction_summary.json`)
- **Processed Files**: Original files are moved to the processed directory after extraction
- **Error Files**: Files with errors are moved to `processed/errors/`

## Unit Test (Testing)

```bash
python -m unittest tests/test_feature_extraction.py
```

## Extending the Tool

### Adding a New LLM Provider

1. Create a new client implementation in `src/llm/`
2. Update the factory in `src/llm/factory.py`

### Customizing Prompts (Prompt Engneering)

Edit the prompt templates in `src/prompts/templates.py`
Additional info can be added in prompt template.


### Adding New Features

Simply add them to `features/features.txt` file - the system will automatically identify them.


## Key Features of the Application

- **Multi-LLM Provider Support**: Seamlessly integrates with OpenAI, Anthropic, and Groq through a unified interface, allowing users to easily switch between different AI providers without code changes.
- **Structured Data Extraction**: Extracts specific, structured features from unstructured product descriptions, converting free-form text into normalized, typed data (numbers, booleans, text) for analysis.
- **Parallel Batch Processing**: Processes multiple files concurrently with a visual progress bar, significantly improving throughput when working with large product datasets.
- **Flexible Configuration System**: Offers multiple configuration methods (environment variables, YAML config) with clear precedence, making it adaptable to different environments and use cases.
- **Production-Grade Error Handling**: Implements comprehensive error recovery with retry mechanisms, detailed logging, and processing summaries that ensure reliability even when API calls fail.
