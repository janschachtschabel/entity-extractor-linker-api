# API Reference

The Entity Extraction Batch API provides comprehensive endpoints for processing text and generating educational content with advanced educational level distribution support. The API supports German educational system standards (Bildungsstufen) and Bloom's Taxonomy for targeted learning content generation.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required for the API endpoints. However, you need to configure the `OPENAI_API_KEY` environment variable for the service to function.

## Rate Limiting

The API implements rate limiting to prevent abuse:
- **Default**: 100 requests per minute per IP
- **Configurable** via environment variables

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "data": { ... },
  "metadata": { ... },
  "processing_time": 1.23
}
```

## Error Handling

Errors are returned with appropriate HTTP status codes and descriptive messages:

```json
{
  "detail": "Error description",
  "error_type": "ValidationError",
  "timestamp": "2025-06-23T10:30:00Z"
}
```

## Educational Features

### 🎓 Educational Level Distribution
- **German Bildungsstufen**: Elementarbereich, Primarstufe, Sekundarstufe I/II, Hochschule, etc.
- **Bloom's Taxonomy**: Erinnern, Verstehen, Anwenden, Analysieren, Bewerten, Erschaffen
- **Custom Taxonomies**: Support for user-defined educational categories
- **Even Distribution**: Automatic distribution of QA pairs across specified levels
- **Level-Appropriate Content**: Complexity and language adapted to educational level

### 🌍 Multi-Language Support
- **German (de)**: Primary language with German educational standards
- **English (en)**: Secondary language support
- **Educational Context**: Language-specific educational terminology and concepts

### 📚 Educational Content Generation
- **Comprehensive Entity Coverage**: Educational aspects, terminology, historical context
- **Citation Integration**: Wikipedia sources with proper attribution
- **Structured Content**: Markdown format with educational organization

## Endpoints Overview

| Endpoint | Method | Purpose | Educational Features |
|----------|--------|---------|---------------------|
| `/linker` | POST | Extract entities and link to Wikipedia | Educational entity generation, multi-perspective coverage |
| `/compendium` | POST | Generate educational content | Educational markdown with citations and structured content |
| `/qa` | POST | Create question-answer pairs | **Educational level distribution**, complexity adaptation |
| `/pipeline` | POST | Complete end-to-end processing | **Full educational pipeline** with level-distributed QA |
| `/utils/synonyms` | POST | Generate synonyms for terms | Educational terminology support |

## Content Types

All endpoints accept and return `application/json` content type.
