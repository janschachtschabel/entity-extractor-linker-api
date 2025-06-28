# Educational Levels QA Generation Guide

Die QA-Funktionalität unterstützt die Generierung von Frage-Antwort-Paaren, die gleichmäßig auf verschiedene Bildungsstufen oder Taxonomien verteilt werden. Diese Anleitung erklärt die verfügbaren Optionen und deren Verwendung.

## Unterstützte Taxonomien

### 1. Deutsche Bildungsstufen (Standard)

Das deutsche Bildungssystem wird vollständig unterstützt mit folgenden Standardstufen:

| Bildungsstufe | Beschreibung | Sprachliche Anpassung |
|---------------|--------------|----------------------|
| **Elementarbereich** | Kindergarten, Vorschule | Sehr einfache Sprache, spielerische Fragen, bildhafte Erklärungen |
| **Primarstufe** | Grundschule (Klassen 1-4) | Einfache Sprache, grundlegende Konzepte, anschauliche Beispiele |
| **Sekundarstufe I** | Hauptschule, Realschule, Gymnasium (Klassen 5-10) | Altersgerechte Sprache, systematischer Aufbau |
| **Sekundarstufe II** | Gymnasium Oberstufe, Berufsschule (Klassen 11-13) | Differenzierte Sprache, wissenschaftspropädeutisch |
| **Hochschule** | Universität, Fachhochschule | Fachsprache, komplexe Zusammenhänge, wissenschaftliche Tiefe |
| **Berufliche Bildung** | Ausbildung, Weiterbildung | Praxisbezug, anwendungsorientierte Fragen |
| **Erwachsenenbildung** | Volkshochschule, Fernstudium | Lebenserfahrung berücksichtigend, selbstgesteuert |
| **Förderschule** | Sonderpädagogische Förderung | Besonders einfache Sprache, kleinschrittig |

### 2. Bloomsche Taxonomie

Die kognitive Taxonomie nach Benjamin Bloom wird mit folgenden Stufen unterstützt:

| Bloom-Stufe | Kognitive Anforderung | Beispiel-Fragetypen |
|-------------|----------------------|-------------------|
| **Erinnern** | Faktenwissen abrufen | "Was ist...?", "Nennen Sie..." |
| **Verstehen** | Bedeutung erfassen | "Erklären Sie...", "Was bedeutet...?" |
| **Anwenden** | Wissen in neuen Situationen nutzen | "Wie würden Sie...?", "Berechnen Sie..." |
| **Analysieren** | Zusammenhänge erkennen | "Warum...?", "Welche Faktoren...?" |
| **Bewerten** | Kritisch beurteilen | "Bewerten Sie...", "Was ist besser...?" |
| **Erschaffen** | Neue Lösungen entwickeln | "Entwerfen Sie...", "Wie könnte man...?" |

### 3. Benutzerdefinierte Kategorien

Sie können auch eigene Kategorien definieren, z.B.:
- **Schwierigkeitsgrade**: ["Anfänger", "Fortgeschritten", "Experte"]
- **Fachbereiche**: ["Theorie", "Praxis", "Anwendung"]
- **Zielgruppen**: ["Schüler", "Studenten", "Fachkräfte"]

## API-Verwendung

### Direkte QA-Endpoint Nutzung

```json
{
  "text": "Ihr Lerninhalt...",
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

### Pipeline-Integration

```json
{
  "text": "Einstein und die Relativitätstheorie",
  "config": {
    "linker": {
      "MODE": "generate",
      "EDUCATIONAL_MODE": true
    },
    "compendium": {
      "length": 6000,
      "educational_mode": true
    },
    "qa": {
      "num_pairs": 16,
      "level_property": "Bildungsstufe",
      "level_values": [
        "Elementarbereich",
        "Primarstufe",
        "Sekundarstufe I",
        "Sekundarstufe II",
        "Hochschule",
        "Berufliche Bildung",
        "Erwachsenenbildung",
        "Förderschule"
      ]
    }
  }
}
```

### Bloomsche Taxonomie Beispiel

```json
{
  "text": "Photosynthese-Inhalt...",
  "num_pairs": 12,
  "level_property": "Bloom_Taxonomie",
  "level_values": [
    "Erinnern",
    "Verstehen",
    "Anwenden", 
    "Analysieren",
    "Bewerten",
    "Erschaffen"
  ]
}
```

## Response-Format

Jedes QA-Paar enthält die Bildungsstufen-Metadaten:

```json
{
  "original_text": "...",
  "qa": [
    {
      "question": "Was ist Quantenphysik?",
      "answer": "Quantenphysik beschreibt das Verhalten von Materie...",
      "level_property": "Bildungsstufe",
      "level_value": "Sekundarstufe II"
    },
    {
      "question": "Wie funktioniert ein Laser?",
      "answer": "Ein Laser erzeugt kohärentes Licht durch...",
      "level_property": "Bildungsstufe", 
      "level_value": "Hochschule"
    }
  ]
}
```

## Verteilungsalgorithmus

Die QA-Paare werden **gleichmäßig** auf die angegebenen Stufen verteilt:

- **12 Paare, 4 Stufen**: 3 Paare pro Stufe
- **10 Paare, 3 Stufen**: 3, 3, 4 Paare (Rest wird gleichmäßig verteilt)
- **16 Paare, 8 Stufen**: 2 Paare pro Stufe

## Best Practices

### 1. Stufenauswahl
- **Zielgruppenspezifisch**: Wählen Sie nur relevante Bildungsstufen
- **Ausgewogen**: 3-6 Stufen für optimale Verteilung
- **Konsistent**: Verwenden Sie einheitliche Bezeichnungen

### 2. Anzahl der QA-Paare
- **Mindestens**: 2 Paare pro Stufe
- **Optimal**: 3-4 Paare pro Stufe
- **Maximum**: 20 Paare insgesamt (API-Limit)

### 3. Inhaltliche Vorbereitung
- **Reichhaltiger Input**: Ausführliche Texte für bessere Differenzierung
- **Fachliche Tiefe**: Verschiedene Komplexitätsebenen im Quelltext
- **Strukturierung**: Klare Gliederung unterstützt stufengerechte Fragen

## Beispiel-Workflows

### Workflow 1: Schulische Differenzierung
```bash
# Für eine Unterrichtseinheit "Klimawandel"
curl -X POST "http://localhost:8000/api/v1/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Klimawandel-Lerninhalt...",
    "num_pairs": 12,
    "level_property": "Bildungsstufe",
    "level_values": ["Sekundarstufe I", "Sekundarstufe II", "Hochschule"]
  }'
```

### Workflow 2: Kognitive Differenzierung
```bash
# Für Bloom-basierte Lernziele
curl -X POST "http://localhost:8000/api/v1/qa" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Fachinhalt...",
    "num_pairs": 18,
    "level_property": "Bloom_Taxonomie", 
    "level_values": ["Erinnern", "Verstehen", "Anwenden", "Analysieren", "Bewerten", "Erschaffen"]
  }'
```

### Workflow 3: Vollständige Pipeline
```bash
# Komplette Inhaltserstellung mit Bildungsstufen
curl -X POST "http://localhost:8000/api/v1/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Quantencomputing",
    "config": {
      "linker": {"MODE": "generate", "EDUCATIONAL_MODE": true},
      "compendium": {"length": 8000, "educational_mode": true},
      "qa": {
        "num_pairs": 16,
        "level_property": "Bildungsstufe",
        "level_values": ["Sekundarstufe II", "Hochschule", "Berufliche Bildung"]
      }
    }
  }'
```

## Fehlerbehebung

### Häufige Probleme

1. **Ungleichmäßige Verteilung**
   - Ursache: Zu wenige QA-Paare für zu viele Stufen
   - Lösung: Mindestens 2 Paare pro Stufe einplanen

2. **Unpassende Stufenzuordnung**
   - Ursache: KI ordnet Stufen falsch zu
   - Lösung: Automatische Korrektur durch Ähnlichkeitsmatching

3. **Fehlende Differenzierung**
   - Ursache: Quelltext zu einfach oder zu komplex
   - Lösung: Ausgewogeneren Input-Text verwenden

### Logging und Debugging

```python
import logging
logging.getLogger("app.core.qa").setLevel(logging.DEBUG)
```

Aktiviert detaillierte Logs für:
- Verteilungsberechnung
- Prompt-Erstellung
- OpenAI-Responses
- Parsing-Ergebnisse

## Erweiterungsmöglichkeiten

Die Architektur unterstützt einfache Erweiterungen:

1. **Neue Taxonomien**: Einfach in `_create_educational_levels_prompt()` hinzufügen
2. **Sprachunterstützung**: Mehrsprachige Bildungsstufen-Definitionen
3. **Adaptive Verteilung**: Intelligente Anpassung basierend auf Inhaltsanalyse
4. **Qualitätsbewertung**: Automatische Bewertung der Stufengerechtigkeit

---

*Diese Dokumentation wird kontinuierlich aktualisiert. Bei Fragen oder Verbesserungsvorschlägen erstellen Sie bitte ein Issue im Repository.*
