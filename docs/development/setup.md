# Development Setup

This guide will help you set up the development environment for the Entity Extraction Batch API.

## Prerequisites

- **Python 3.13+** (recommended)
- **Git** for version control
- **Docker** (optional, for containerized development)
- **OpenAI API Key** for LLM functionality

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/entityextractorbatch.git
cd entityextractorbatch
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or using conda
conda create -n entityextractor python=3.13
conda activate entityextractor
```

### 3. Install Dependencies

```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_TIMEOUT=60.0

# Application Settings
DEBUG=true
LOG_LEVEL=DEBUG

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_WINDOW=60

# Wikipedia API
WIKIPEDIA_TIMEOUT=30.0
```

### 5. Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
pre-commit install
```

This will automatically run:
- Ruff linting and formatting
- MyPy type checking
- YAML/TOML validation
- Pytest (on commit)

## Running the Application

### Development Server

```bash
# Start with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the provided script
python -m app.main
```

### Docker Development

```bash
# Build development image
docker build -t entityextractorbatch:dev .

# Run with environment variables
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e DEBUG=true \
  entityextractorbatch:dev
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_linker.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── test_endpoints.py      # API endpoint tests
├── test_linker.py         # Entity linking tests
├── test_compendium.py     # Content generation tests
├── test_qa.py             # Q&A generation tests
├── test_pipeline.py       # Pipeline orchestration tests
├── test_utils.py          # Utility function tests
└── test_wikipedia_service.py # Wikipedia service tests
```

## Code Quality

### Linting and Formatting

```bash
# Check code quality
ruff check app/

# Auto-fix issues
ruff check app/ --fix

# Format code
ruff format app/

# Type checking
mypy app/
```

### Code Quality Standards

- **Line Length**: 120 characters maximum
- **Import Sorting**: Automatic with ruff
- **Type Hints**: Required for all functions
- **Docstrings**: PEP 257 format for all public functions
- **Error Handling**: Custom exceptions with proper logging

## Documentation

### Building Documentation

```bash
# Install documentation dependencies (included in dev dependencies)
pip install -e ".[dev]"

# Build documentation
mkdocs build

# Serve locally with auto-reload
mkdocs serve
```

### Documentation Structure

```
docs/
├── index.md               # Main documentation page
├── api/                   # API documentation
│   ├── overview.md        # API overview
│   └── endpoints.md       # Detailed endpoint docs
├── architecture/          # Architecture documentation
│   └── overview.md        # System architecture
└── development/           # Development guides
    └── setup.md           # This file
```

## Contributing

### Workflow

1. **Create Feature Branch**: `git checkout -b feature/your-feature`
2. **Make Changes**: Follow code quality standards
3. **Run Tests**: Ensure all tests pass
4. **Commit Changes**: Pre-commit hooks will run automatically
5. **Push Branch**: `git push origin feature/your-feature`
6. **Create Pull Request**: Use the provided PR template

### Code Review Checklist

- [ ] All tests pass
- [ ] Code coverage maintained
- [ ] Type hints added
- [ ] Docstrings updated
- [ ] No linting errors
- [ ] Documentation updated if needed

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall in development mode
pip install -e ".[dev]"
```

**OpenAI API Errors**
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

**Docker Issues**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t entityextractorbatch .
```

### Getting Help

- Check the [API documentation](../api/overview.md)
- Review [architecture overview](../architecture/overview.md)
- Open an issue on GitHub
- Contact the development team
