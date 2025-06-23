# API Reference

The Entity Extraction Batch API provides four main endpoints for processing text and generating educational content.

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

## Endpoints Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/linker` | POST | Extract entities and link to Wikipedia |
| `/compendium` | POST | Generate educational content |
| `/qa` | POST | Create question-answer pairs |
| `/pipeline` | POST | Complete end-to-end processing |
| `/utils/synonyms` | POST | Generate synonyms for terms |

## Content Types

All endpoints accept and return `application/json` content type.
