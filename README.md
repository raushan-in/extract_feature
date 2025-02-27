# Feature Extraction Tool

A tool for extracting structured features from product descriptions using LLM.

## Architecture

```
feature_extraction/
├── src/                     # Source code
│   ├── config/               # Configuration management
│   ├── llm/                 # LLM client implementations
│   ├── models/              # Data models and schemas
│   ├── processors/          # Processing logic
│   ├── prompts/             # LLM prompt templates
│   ├── utils/               # Utility functions
│   └── main.py              # Entry point
```

## Setup

1. virtual environment

# Create
```bash
python -m venv venv
```

# On Windows:
```bash
venv\Scripts\activate
```

# On macOS/Linux:
```bash
source venv/bin/activate
```

2. Install the package:

```bash
pip install -e .
```

3. Configure your API key:

   - Copy `.env.sample` to `.env`
   - Uncomment and add your API key for the service you'll use

# Regular useses

4. Place your product files in the input directory (default: `input_files/`)


### Basic Usage

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
| LLM Provider | `LLM_PROVIDER` | `openai` | LLM API provider (openai, anthropic, groq) |
| LLM Model | `LLM_MODEL` | *provider default* | Specific model to use |
| Features File | `FEATURES_FILE` | `features.txt` | Path to features definition file |
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

## Extending the Tool

### Adding a New LLM Provider

1. Create a new client implementation in `src/llm/`
2. Update the factory in `src/llm/factory.py`

### Customizing Prompts

Edit the prompt templates in `src/prompts/templates.py`

### Adding New Features

Simply add them to your `features.txt` file - the system will automatically generate models for them.
