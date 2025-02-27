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