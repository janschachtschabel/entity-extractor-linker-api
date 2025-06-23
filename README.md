# Entity Extraction Batch API

[![CI/CD Pipeline](https://github.com/janschachtschabel/entity-extractor-linker-api/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/janschachtschabel/entity-extractor-linker-api/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-green.svg)](https://github.com/janschachtschabel/entity-extractor-linker-api)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive entity extraction and knowledge API with Wikipedia linking, educational content generation, and question-answer pair creation. Built with modern Python standards and production-ready architecture.

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** (recommended)
- **OpenAI API Key** for LLM functionality
- **Docker** (optional, for containerized deployment)

### Installation

```bash
# Clone repository
git clone https://github.com/janschachtschabel/entity-extractor-linker-api.git
cd entity-extractor-linker-api

# Install with development dependencies
pip install -e ".[dev]"

# Set up environment variables
export OPENAI_API_KEY="your-openai-api-key"

# Run the application
uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build and run
docker build -t entityextractorbatch .
docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" entityextractorbatch

# Health check
curl http://localhost:8000/health
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/linker` | POST | Entity extraction and Wikipedia linking |
| `/api/v1/compendium` | POST | Educational content generation |
| `/api/v1/qa` | POST | Question-answer pair creation |
| `/api/v1/pipeline` | POST | **Complete pipeline orchestration** |
| `/api/v1/utils/synonyms` | POST | Synonym generation utility |
| `/health` | GET | Health check endpoint |

**📖 Interactive Documentation**: Visit `/docs` for Swagger UI or `/redoc` for ReDoc

## 🏗️ Architecture

Modern, modular architecture with clear separation of concerns:

```
app/
├── api/v1/              # API endpoints (FastAPI routers)
├── core/                # Business logic and utilities
├── models/              # Pydantic data models
├── services/            # External service integrations
│   └── wikipedia/       # Wikipedia API service
└── main.py              # Application factory
```

**Key Features:**
- ✅ **Async/Await**: Non-blocking I/O operations
- ✅ **Type Safety**: Full MyPy type checking
- ✅ **Error Handling**: Custom exception hierarchy
- ✅ **Rate Limiting**: Built-in request throttling
- ✅ **Health Checks**: Docker-ready monitoring
- ✅ **Logging**: Structured logging with Loguru

## 📚 Documentation

- **[API Reference](docs/api/overview.md)** - Detailed endpoint documentation
- **[Architecture Overview](docs/architecture/overview.md)** - System design and patterns
- **[Development Setup](docs/development/setup.md)** - Complete development guide
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)

## 🔧 Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### Code Quality Standards

```bash
# Linting and formatting
ruff check app/ --fix
ruff format app/

# Type checking
mypy app/

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Quality Assurance

- **Ruff**: Linting and formatting with 120-character line limit
- **MyPy**: Strict type checking enabled
- **Pre-commit**: Automated quality checks on commit
- **Pytest**: Comprehensive test suite with 15+ tests
- **GitHub Actions**: CI/CD pipeline with quality gates

## 🐳 Production Deployment

### Docker Production Setup

```bash
# Multi-stage production build
docker build -t entityextractorbatch:prod .

# Run with production settings
docker run -d \
  --name entityextractor-prod \
  -p 8000:8000 \
  -e OPENAI_API_KEY="your-production-key" \
  -e LOG_LEVEL="WARNING" \
  --restart unless-stopped \
  entityextractorbatch:prod
```

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `OPENAI_API_KEY` | Required for LLM functionality | *(required)* |
| `OPENAI_TIMEOUT` | Request timeout for OpenAI API | `60.0` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `RATE_LIMIT_REQUESTS` | Requests per minute per IP | `100` |
| `RATE_WINDOW` | Rate limiting window in seconds | `60` |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/test_endpoints.py  # API tests
pytest tests/test_linker.py     # Entity linking tests
pytest tests/test_pipeline.py  # Pipeline orchestration tests
```

**Test Coverage**: 15+ comprehensive tests covering all major functionality

## 📈 Performance

### Pipeline Benchmarks

- **Entity Extraction**: ~5-15 seconds (depending on text complexity)
- **Wikipedia Linking**: ~2-8 seconds (with intelligent fallbacks)
- **Content Generation**: ~20-40 seconds (for 5000+ word content)
- **Q&A Generation**: ~3-8 seconds (for 10+ question pairs)

### Optimization Features

- **Async Processing**: Concurrent Wikipedia API calls
- **Intelligent Caching**: Reduces redundant API requests
- **Fallback Strategies**: Multiple approaches for entity linking
- **Rate Limiting**: Prevents API abuse and ensures stability

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/development/setup.md) for details.

### Contribution Workflow

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following our code quality standards
4. **Run tests**: `pytest` and quality checks: `ruff check app/`
5. **Commit changes**: Pre-commit hooks will run automatically
6. **Push branch**: `git push origin feature/amazing-feature`
7. **Create Pull Request** with detailed description

### Code Quality Requirements

- ✅ All tests must pass
- ✅ Code coverage maintained
- ✅ Ruff linting with no errors
- ✅ MyPy type checking passes
- ✅ Docstrings for all public functions
- ✅ Maximum 120 characters per line

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Full documentation](docs/index.md)
- **Issues**: [GitHub Issues](https://github.com/janschachtschabel/entity-extractor-linker-api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/janschachtschabel/entity-extractor-linker-api/discussions)

---

**Built with ❤️ using modern Python standards and production-ready architecture.**
