"""Utility helper functions: split, synonyms, translate.

These are lightweight placeholders to satisfy the MVP util endpoints. They can
later be replaced with more sophisticated implementations or external APIs.
"""

from __future__ import annotations

import re

from loguru import logger

# Logging via loguru (see plan.md for style)


def _clean_text_for_json(text: str) -> str:
    """Clean text to be JSON-safe by removing/replacing invalid control characters."""
    if not text:
        return text

    # Remove or replace problematic control characters
    # Keep common whitespace characters (space, tab, newline, carriage return)
    cleaned = ""
    for char in text:
        # Allow printable characters and common whitespace
        if char.isprintable() or char in "\t\n\r":
            cleaned += char
        else:
            # Replace control characters with space
            cleaned += " "

    # Normalize multiple whitespace to single spaces
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def split_text(
    text: str,
    chunk_size: int = 200,
    *,
    overlap: int = 0,
    by: str = "sentence",
) -> list[str]:
    logger.info(f"[split_text] Called with chunk_size={chunk_size}, overlap={overlap}, by='{by}'")
    logger.debug(f"[split_text] Input text length: {len(text) if text else 0}")
    """Split *text* into chunks.

    Parameters
    ----------
    text : str
        Input string.
    chunk_size : int, default 200
        Target size of each chunk (characters).
    overlap : int, default 0
        If >0, create overlapping context of *overlap* characters between
        consecutive chunks (only for `by="char"`).
    by : {"sentence", "char"}, default "sentence"
        Split logic:
        • "sentence": build chunks by concatenating whole sentences until the
          size limit is reached (legacy behaviour).
        • "char": split purely by character count (useful for LLM windowing).
    """
    text = text.strip()
    if not text:
        logger.info("[split_text] Empty input text. Returning empty list.")
        return []

    if by == "char":
        if chunk_size <= 0:
            logger.error(f"[split_text] Invalid chunk_size: {chunk_size}")
            raise ValueError("chunk_size must be positive")
        if overlap < 0 or overlap >= chunk_size:
            logger.error(f"[split_text] Invalid overlap: {overlap} (chunk_size={chunk_size})")
            raise ValueError("0 <= overlap < chunk_size required")
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(_clean_text_for_json(text[start:end]))
            start = end - overlap  # move with overlap
        logger.info(f"[split_text] Returning {len(chunks)} chunks (char mode)")
        return chunks

    # sentence mode (default)
    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks: list[str] = []
    current = ""
    last_sentences = []  # Keep track of sentences in current chunk

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        if len(current) + len(s) + 1 <= chunk_size:
            current += (" " if current else "") + s
            last_sentences.append(s)
        else:
            if current:
                chunks.append(_clean_text_for_json(current))

            # Handle overlap for sentence mode
            if overlap > 0 and last_sentences:
                # Add sentences from previous chunk until we reach desired overlap
                overlap_text = ""
                i = len(last_sentences) - 1

                while i >= 0 and len(overlap_text) < overlap:
                    overlap_text = last_sentences[i] + (" " + overlap_text if overlap_text else "")
                    i -= 1

                # Start new chunk with overlap text
                if overlap_text:
                    current = overlap_text + " " + s
                    last_sentences = [s]
                    if i >= 0:  # Add sentences used for overlap
                        last_sentences = last_sentences[i + 1 :] + last_sentences
                else:
                    current = s
                    last_sentences = [s]
            else:
                current = s
                last_sentences = [s]

    if current:
        chunks.append(_clean_text_for_json(current))
    logger.info(f"[split_text] Returning {len(chunks)} chunks (sentence mode)")
    return chunks


_simple_synonyms = {
    "Berg": ["Gebirge", "Erhebung"],
    "hoch": ["groß", "erhaben"],
}


from .openai_wrapper import generate_synonyms_llm as _synonyms_llm


def generate_synonyms(word: str, max_synonyms: int = 5, *, lang: str = "de") -> list[str]:
    """Return synonyms via OpenAI – fallback to local dict."""
    logger.info(f"[generate_synonyms] Called with word='{word}', max_synonyms={max_synonyms}, lang='{lang}'")
    try:
        syns = _synonyms_llm(word, max_synonyms=max_synonyms, lang=lang)
        if syns:
            logger.info(f"[generate_synonyms] Found {len(syns)} synonyms via OpenAI for '{word}'")
            return syns
    except Exception as exc:
        logger.warning(f"[generate_synonyms] OpenAI fallback for word '{word}': {exc}")
    fallback_syns = _simple_synonyms.get(word, [])[:max_synonyms]
    logger.info(f"[generate_synonyms] Returning {len(fallback_syns)} fallback synonyms for '{word}'")
    return fallback_syns


from .openai_wrapper import translate_text as _translate_text


def translate(text: str, target_lang: str = "en", source_lang: str = None) -> str:
    logger.info(f"[translate] Called with target_lang='{target_lang}', source_lang='{source_lang}'")
    logger.debug(f"[translate] Input text length: {len(text) if text else 0}")
    """Translate *text* to *target_lang* via OpenAI.

    Parameters
    ----------
    text : str
        Text to translate
    target_lang : str, default "en"
        Target language code (e.g., "en", "de")
    source_lang : str, optional
        Source language code if known

    Returns
    -------
    str
        Translated text or fallback message if translation fails

    Falls back to returning the original text if OpenAI is not configured.
    """
    try:
        # Pass source_lang if provided
        kwargs = {"target_lang": target_lang}
        if source_lang:
            kwargs["source_lang"] = source_lang

        out = _translate_text(text, **kwargs)

        if out and out.strip() != text.strip():  # Check for actual translation
            logger.info(f"[translate] Successfully translated text to '{target_lang}'")
            return out
        logger.info(f"[translate] No translation performed, returning fallback for '{target_lang}'")
        return f"[{target_lang} translation of]: {text}"
    except Exception as exc:  # Catch any exception for robustness
        logger.warning(f"[translate] OpenAI fallback for target_lang='{target_lang}': {exc}")
        return f"[{target_lang} translation of]: {text}"
