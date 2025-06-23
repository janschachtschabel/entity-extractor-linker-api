"""Generate question/answer pairs from compendium markdown."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def generate_qa_pairs(
    markdown: str, num_pairs: int = 5, topic: str = None, max_chars: int = None
) -> list[tuple[str, str]]:
    """Return list of (question, answer) tuples.

    Parameters
    ----------
    markdown : str
        Markdown content to generate QA pairs from
    num_pairs : int, default 5
        Number of QA pairs to generate
    topic : str, optional
        Specific topic to focus questions on
    max_chars : int, optional
        Maximum character length for each answer

    Raises
    ------
    RuntimeError
        If OpenAI is not available or configured properly
    ValueError
        If OpenAI returns invalid or empty response
    """
    logger.info(f"[generate_qa_pairs] Called with num_pairs={num_pairs}, max_chars={max_chars}")

    try:
        # Einfacher Prompt für Semikolon-Format
        prompt = (
            "Du bist ein Assistent, der Lernfragen erstellt. "
            f"Erstelle basierend auf dem folgenden Text GENAU {num_pairs} verschiedene Frage-Antwort-Paare. "
            "WICHTIG: Antworte NUR mit den Frage-Antwort-Paaren im folgenden Format:\n\n"
            "Frage 1;Antwort 1\n"
            "Frage 2;Antwort 2\n"
            "Frage 3;Antwort 3\n\n"
            "Jedes Paar in eine neue Zeile, getrennt durch Semikolon. "
            "Keine zusätzlichen Erklärungen, keine Nummerierung, keine Markdown-Formatierung.\n"
            f"ANZAHL PAARE: {num_pairs}\n"
        )

        if topic:
            prompt += f"SCHWERPUNKT: {topic}\n"

        if max_chars:
            prompt += f"MAX ANTWORTLÄNGE: {max_chars} Zeichen\n"

        prompt += f"\nTEXT:\n{markdown}\n\n"
        prompt += f"Erstelle nun {num_pairs} Frage-Antwort-Paare:"

        logger.debug(f"[generate_qa_pairs] Calling OpenAI with prompt length: {len(prompt)}")

        # Call OpenAI with our enhanced prompt
        pairs = _call_openai_generate(prompt, num_pairs, max_chars)
        if pairs:
            logger.info(f"[generate_qa_pairs] OpenAI returned {len(pairs)} QA pairs")
            return pairs
        else:
            logger.error("[generate_qa_pairs] OpenAI returned empty result")
            raise ValueError("OpenAI returned empty or invalid response for QA generation")

    except Exception as exc:  # pylint: disable=broad-except
        logger.error(f"[generate_qa_pairs] OpenAI QA generation failed: {type(exc).__name__}: {exc}")
        # Re-raise the exception instead of using fallback
        if isinstance(exc, (RuntimeError, ValueError)):
            raise
        else:
            raise RuntimeError(f"QA generation failed: {exc}") from exc


def _call_openai_generate(prompt: str, num_pairs: int, max_chars: int = None) -> list[tuple[str, str]]:
    """Direct OpenAI chat call wrapped for QA generation."""
    from . import openai_wrapper  # reuse ensure_ready & openai import

    logger.debug(f"[_call_openai_generate] Starting OpenAI call for {num_pairs} pairs")

    openai_wrapper._ensure_ready()  # type: ignore
    openai = openai_wrapper.openai  # type: ignore

    response = openai.chat.completions.create(  # type: ignore[attr-defined]
        model=openai_wrapper.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # Etwas mehr Kreativität
        max_tokens=2000,  # Mehr Tokens für mehrere Paare
    )

    content = response.choices[0].message.content  # type: ignore[index]
    logger.debug(f"[_call_openai_generate] OpenAI raw response: {content}")

    try:
        # Einfache Bereinigung für Semikolon-Format
        cleaned_content = content.strip()
        # Entferne mögliche Code-Fences
        if cleaned_content.startswith("```"):
            lines = cleaned_content.split("\n")
            cleaned_content = "\n".join(lines[1:-1]) if len(lines) > 2 else cleaned_content

        logger.debug(f"[_call_openai_generate] Cleaned content: {cleaned_content}")

        # Semikolon-Format direkt parsen
        pairs = []
        for line in cleaned_content.splitlines():
            line = line.strip()
            if ";" in line and line:
                parts = line.split(";", 1)
                if len(parts) == 2:
                    q, a = parts
                    q = q.strip()
                    a = a.strip()

                    if q and a:  # Beide müssen vorhanden sein
                        if max_chars and len(a) > max_chars:
                            a = a[: max_chars - 3] + "..."
                        pairs.append((q, a))
                        logger.debug(f"[_call_openai_generate] Added pair: '{q}' -> '{a[:50]}...'")

        logger.info(f"[_call_openai_generate] Successfully extracted {len(pairs)} QA pairs (requested: {num_pairs})")

        # Warnung falls weniger Paare als erwartet
        if len(pairs) < num_pairs:
            logger.warning(f"[_call_openai_generate] Only got {len(pairs)} pairs instead of requested {num_pairs}")

        return pairs

    except Exception as e:
        logger.error(f"[_call_openai_generate] Error processing OpenAI response: {e}")
        return []
