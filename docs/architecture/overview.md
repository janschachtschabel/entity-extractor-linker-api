# Architecture Overview

The Entity Extraction Batch API follows a modern, modular architecture designed for maintainability, scalability, and testability.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Layer     │    │   Core Logic    │    │    Services     │
│                 │    │                 │    │                 │
│ • FastAPI       │◄──►│ • Entity Proc. │◄──►│ • Wikipedia     │
│ • Pydantic     │    │ • Content Gen.  │    │ • OpenAI        │
│ • Rate Limiting │    │ • QA Generation │    │ • HTTP Clients  │
│ • Validation    │    │ • Pipeline Orch.│    │ • External APIs │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Models      │
                    │                 │
                    │ • Data Schemas  │
                    │ • Validation    │
                    │ • Serialization │
                    └─────────────────┘
```

## Directory Structure

```
app/
├── api/                    # API layer
│   └── v1/                # API version 1
│       ├── linker.py      # Entity linking endpoint
│       ├── compendium.py  # Content generation endpoint
│       ├── qa.py          # Q&A generation endpoint
│       ├── pipeline.py    # Pipeline orchestration
│       └── utils.py       # Utility endpoints
├── core/                  # Core business logic
│   ├── openai_wrapper.py  # OpenAI integration
│   ├── settings.py        # Configuration
│   └── utils.py           # Core utilities
├── models/                # Data models
│   ├── entity_models.py   # Entity-related models
│   ├── compendium_models.py # Content models
│   └── qa_models.py       # Q&A models
└── services/              # External services
    └── wikipedia/         # Wikipedia service
        ├── api/           # Wikipedia API client
        ├── fallbacks/     # Fallback strategies
        ├── utils/         # Wikipedia utilities
        └── service.py     # Main service class
```

## Design Principles

### 1. Separation of Concerns
- **API Layer**: Handles HTTP requests, validation, and responses
- **Core Logic**: Contains business logic and processing algorithms
- **Services**: Manages external API integrations
- **Models**: Defines data structures and validation rules

### 2. Dependency Injection
- Services are injected into endpoints
- Easy to mock for testing
- Configurable via environment variables

### 3. Async/Await Pattern
- Non-blocking I/O operations
- Concurrent processing where possible
- Efficient resource utilization

### 4. Error Handling
- Custom exception hierarchy
- Proper error propagation
- Detailed logging with structured data

## Data Flow

### Entity Linking Pipeline
1. **Input Validation**: Pydantic models validate request data
2. **Entity Extraction**: OpenAI extracts/generates entities from text
3. **Wikipedia Linking**: Entities are linked to Wikipedia articles
4. **Fallback Strategies**: Multiple strategies for difficult entities
5. **Response Formatting**: Structured response with metadata

### Content Generation Pipeline
1. **Entity Processing**: Takes linked entities as input
2. **Content Generation**: OpenAI generates educational content
3. **Citation Integration**: Wikipedia sources are integrated
4. **Markdown Formatting**: Output formatted as structured markdown

### Q&A Generation Pipeline
1. **Content Analysis**: Analyzes markdown content structure
2. **Question Generation**: Creates relevant questions
3. **Answer Extraction**: Generates concise answers
4. **Quality Validation**: Ensures Q&A pair quality

## Scalability Considerations

### Horizontal Scaling
- Stateless design enables easy horizontal scaling
- No shared state between requests
- Database-free architecture (external APIs only)

### Performance Optimization
- Async HTTP clients for external API calls
- Connection pooling for Wikipedia API
- Intelligent caching strategies
- Rate limiting to prevent abuse

### Monitoring & Observability
- Structured logging with Loguru
- Health check endpoints
- Processing time metrics
- Error tracking and reporting
