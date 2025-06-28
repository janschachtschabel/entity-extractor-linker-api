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

Generate question-answer pairs from text content, with optional educational level distribution.

**Request Body (Standard):**
```json
{
  "text": "# Einstein\n\nAlbert Einstein war ein deutscher theoretischer Physiker...",
  "num_pairs": 10,
  "max_answer_length": 200
}
```

**Request Body (Mit Bildungsstufen):**
```json
{
  "text": "# Quantenphysik\n\nDie Quantenphysik beschreibt...",
  "num_pairs": 12,
  "max_answer_length": 250,
  "level_property": "Bildungsstufe",
  "level_values": [
    "Primarstufe",
    "Sekundarstufe I",
    "Sekundarstufe II", 
    "Hochschule"
  ]
}
```

**Request Body (Bloomsche Taxonomie):**
```json
{
  "text": "# Photosynthese\n\nDie Photosynthese ist...",
  "num_pairs": 12,
  "max_answer_length": 200,
  "level_property": "Bloom_Taxonomie",
  "level_values": [
    "Erinnern",
    "Verstehen",
    "Anwenden",
    "Analysieren"
  ]
}
```

**Response:**
```json
{
  "original_text": "# Quantenphysik...",
  "qa": [
    {
      "question": "Was ist Quantenphysik?",
      "answer": "Quantenphysik ist ein Bereich der Physik...",
      "level_property": "Bildungsstufe",
      "level_value": "Sekundarstufe I"
    },
    {
      "question": "Wie funktioniert die Unschärferelation?",
      "answer": "Die Heisenbergsche Unschärferelation besagt...",
      "level_property": "Bildungsstufe",
      "level_value": "Hochschule"
    }
  ]
}
```

**Parameter:**
- `text`: Eingabetext (Markdown unterstützt)
- `num_pairs`: Anzahl QA-Paare (1-20)
- `max_answer_length`: Max. Antwortlänge (50-1000 Zeichen)
- `level_property`: Name der Bildungsstufen-Eigenschaft (optional)
- `level_values`: Liste der Bildungsstufen-Werte (optional)

**Deutsche Bildungsstufen (Standard):**
`["Elementarbereich", "Primarstufe", "Sekundarstufe I", "Sekundarstufe II", "Hochschule", "Berufliche Bildung", "Erwachsenenbildung", "Förderschule"]`

**Bloomsche Taxonomie:**
`["Erinnern", "Verstehen", "Anwenden", "Analysieren", "Bewerten", "Erschaffen"]`

## Pipeline Endpoint

### `POST /api/v1/pipeline`

Complete end-to-end processing combining all three endpoints.

**Request Body (Standard):**
```json
{
  "text": "Einstein und die Relativitätstheorie",
  "config": {
    "linker": { 
      "MODE": "generate", 
      "MAX_ENTITIES": 15,
      "EDUCATIONAL_MODE": true
    },
    "compendium": { 
      "length": 8000, 
      "enable_citations": true,
      "educational_mode": true
    },
    "qa": { 
      "num_pairs": 12, 
      "max_answer_length": 300 
    }
  }
}
```

**Request Body (Mit Bildungsstufen):**
```json
{
  "text": "Quantencomputing und künstliche Intelligenz",
  "config": {
    "linker": {
      "MODE": "generate",
      "MAX_ENTITIES": 20,
      "EDUCATIONAL_MODE": true,
      "LANGUAGE": "de"
    },
    "compendium": {
      "length": 10000,
      "enable_citations": true,
      "educational_mode": true,
      "language": "de"
    },
    "qa": {
      "num_pairs": 16,
      "max_answer_length": 300,
      "level_property": "Bildungsstufe",
      "level_values": [
        "Sekundarstufe II",
        "Hochschule",
        "Berufliche Bildung",
        "Erwachsenenbildung"
      ]
    }
  }
}
```

**Response:**
```json
{
  "original_text": "Quantencomputing und künstliche Intelligenz",
  "linker_output": {
    "entities": [...],
    "metadata": {...}
  },
  "compendium_output": {
    "markdown": "# Quantencomputing und KI\n\n...",
    "metadata": {...}
  },
  "qa_output": {
    "original_text": "...",
    "qa": [
      {
        "question": "Was ist ein Quantencomputer?",
        "answer": "Ein Quantencomputer nutzt quantenmechanische...",
        "level_property": "Bildungsstufe",
        "level_value": "Sekundarstufe II"
      },
      {
        "question": "Wie funktioniert Quantenverschränkung?",
        "answer": "Quantenverschränkung beschreibt ein Phänomen...",
        "level_property": "Bildungsstufe",
        "level_value": "Hochschule"
      }
    ]
  },
  "pipeline_statistics": {
    "total_processing_time": 67.4,
    "steps_completed": 3,
    "processing_times": {
      "linker": 18.2,
      "compendium": 41.7,
      "qa": 7.5
    },
    "educational_levels_distribution": {
      "Sekundarstufe II": 4,
      "Hochschule": 4,
      "Berufliche Bildung": 4,
      "Erwachsenenbildung": 4
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
