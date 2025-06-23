import logging
from typing import Any

from ..services.wikipedia.models import WikiPage

logger = logging.getLogger(__name__)

# Hier können Wikipedia-spezifische Hilfsfunktionen ausgelagert werden.


def extract_wikipedia_data(
    wiki_page: dict[str, Any] | WikiPage | None, ctx, dbp_data: dict[str, Any]
) -> dict[str, Any]:
    """Extrahiert Wikipedia-relevante Felder aus WikiPage oder dict."""
    # ... (Platzhalter: Hier kann die Extraktionslogik aus linker.py ausgelagert werden)
    return {}
