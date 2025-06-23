# Entity Extraction & Knowledge API

[![CI/CD Pipeline](https://github.com/janschachtschabel/entity-extractor-linker-api/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/janschachtschabel/entity-extractor-linker-api/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-green.svg)](https://github.com/janschachtschabel/entity-extractor-linker-api)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive entity extraction and knowledge API with Wikipedia linking, educational content generation, and question-answer pair creation.

## Features

- **Entity Extraction**: Extract or generate entities from text using OpenAI-compatible LLMs
- **Wikipedia Linking**: Intelligent entity linking with fallback strategies
- **Educational Content**: Generate comprehensive educational content (Compendium)
- **Q&A Generation**: Create question-answer pairs from content
- **Pipeline Orchestration**: End-to-end processing in a single API call

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/janschachtschabel/entity-extractor-linker-api.git
cd entity-extractor-linker-api

# Install dependencies
pip install -e ".[dev]"

# Set up environment variables
export OPENAI_API_KEY="your-openai-api-key"

# Run the application
uvicorn app.main:app --reload
```

### Docker

```bash
# Build and run with Docker
docker build -t entityextractorbatch .
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" entityextractorbatch
```

## API Endpoints

- **`/api/v1/linker`** - Entity extraction and Wikipedia linking
- **`/api/v1/compendium`** - Educational content generation
- **`/api/v1/qa`** - Question-answer pair generation
- **`/api/v1/pipeline`** - Complete pipeline orchestration
- **`/health`** - Health check endpoint

## Interactive Documentation

Visit `/docs` for Swagger UI or `/redoc` for ReDoc when the application is running.

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **API Layer**: FastAPI endpoints with Pydantic validation
- **Core Logic**: Business logic for entity processing, content generation
- **Services**: External service integrations (Wikipedia, OpenAI)
- **Models**: Data models and schemas

## Development

See the [Development Guide](development/setup.md) for detailed setup instructions and contribution guidelines.
