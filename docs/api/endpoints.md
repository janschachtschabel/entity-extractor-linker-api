# API Endpoints

## Linker Endpoint

### `POST /api/v1/linker`

Extract entities from text and link them to Wikipedia articles.

**Request Body:**
```json
{
  "text": "Einstein entwickelte die Relativitätstheorie",
  "config": {
    "MODE": "extract",
    "MAX_ENTITIES": 10,
    "ALLOWED_ENTITY_TYPES": ["PERSON", "CONCEPT"],
    "EDUCATIONAL_MODE": true,
    "LANGUAGE": "de"
  }
}
```

**Response:**
```json
{
  "entities": [
    {
      "entity": "Albert Einstein",
      "details": "German-born theoretical physicist",
      "sources": {
        "wikipedia": {
          "url_de": "https://de.wikipedia.org/wiki/Albert_Einstein",
          "extract": "Albert Einstein war ein deutscher...",
          "wikidata_id": "Q937"
        }
      },
      "id": "entity_1"
    }
  ],
  "metadata": {
    "total_entities": 1,
    "processing_mode": "extract",
    "language": "de"
  }
}
```

## Compendium Endpoint

### `POST /api/v1/compendium`

Generate educational content from entity data.

**Request Body:**
```json
{
  "entities": [...],
  "config": {
    "length": 5000,
    "enable_citations": true,
    "educational_mode": true,
    "language": "de"
  }
}
```

## QA Endpoint

### `POST /api/v1/qa`

Generate question-answer pairs from markdown content.

**Request Body:**
```json
{
  "markdown_content": "# Einstein\n\nAlbert Einstein war...",
  "config": {
    "num_pairs": 10,
    "max_answer_length": 200
  }
}
```

## Pipeline Endpoint

### `POST /api/v1/pipeline`

Complete end-to-end processing combining all three endpoints.

**Request Body:**
```json
{
  "text": "Input text for processing",
  "config": {
    "linker": { "MODE": "generate", "MAX_ENTITIES": 15 },
    "compendium": { "length": 8000, "enable_citations": true },
    "qa": { "num_pairs": 12, "max_answer_length": 300 }
  }
}
```

**Response:**
```json
{
  "original_text": "Input text",
  "linker_output": { ... },
  "compendium_output": { ... },
  "qa_output": { ... },
  "pipeline_statistics": {
    "total_processing_time": 45.2,
    "steps_completed": 3,
    "step_times": {
      "linker": 12.3,
      "compendium": 28.1,
      "qa": 4.8
    }
  }
}
```

## Utils Endpoints

### `POST /api/v1/utils/synonyms`

Generate synonyms for a given term.

**Request Body:**
```json
{
  "term": "Wissenschaft",
  "max_synonyms": 5
}
```

**Response:**
```json
{
  "term": "Wissenschaft",
  "synonyms": ["Forschung", "Wissenschaftlichkeit", "Gelehrsamkeit"]
}
```
