"""Data processing utilities for Wikipedia service."""

from typing import Any

from loguru import logger

from ..exceptions import WikipediaValidationError
from ..models import WikiPage


class WikipediaDataProcessor:
    """Processes and validates Wikipedia API response data."""

    @staticmethod
    def merge_page_data(wiki_page: WikiPage, page_data: dict[str, Any], lang: str) -> None:
        """
        Merge Wikipedia API page data into a WikiPage object.

        Args:
            wiki_page: WikiPage object to update
            page_data: Raw page data from Wikipedia API
            lang: Language code ('de' or 'en')
        """
        try:
            # Set title based on language
            title = page_data.get("title", "").strip()
            if title:
                if lang == "de":
                    wiki_page.title_de = title
                else:
                    wiki_page.title_en = title

            # Set abstract/extract based on language
            extract = page_data.get("extract", "").strip()
            if extract:
                if lang == "de":
                    wiki_page.abstract_de = extract
                else:
                    wiki_page.abstract_en = extract

            # Set Wikidata ID from pageprops
            pageprops = page_data.get("pageprops", {})
            if isinstance(pageprops, dict):
                wikidata_id = pageprops.get("wikibase_item")
                if wikidata_id and not wiki_page.wikidata_id:
                    wiki_page.wikidata_id = wikidata_id

            # Process categories
            WikipediaDataProcessor._update_categories(wiki_page, page_data)

            # Process coordinates
            WikipediaDataProcessor._update_coordinates(wiki_page, page_data)

            # Process internal links
            WikipediaDataProcessor._update_internal_links(wiki_page, page_data)

            # Process thumbnail
            WikipediaDataProcessor._update_thumbnail(wiki_page, page_data)

            # Update infobox type
            WikipediaDataProcessor._update_infobox_type(wiki_page, page_data)

            # Process language links
            WikipediaDataProcessor._update_langlinks(wiki_page, page_data)

            # Generate URLs
            WikipediaDataProcessor._update_urls(wiki_page, lang)

        except Exception as e:
            logger.error(f"Error merging page data for {lang}: {e}", exc_info=True)
            raise WikipediaValidationError(f"Failed to merge page data: {e}") from e

    @staticmethod
    def _update_categories(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update categories from page data."""
        categories_raw = page_data.get("categories", [])
        if isinstance(categories_raw, list) and not wiki_page.categories:
            wiki_page.categories = [
                cat["title"].replace("Category:", "").replace("Kategorie:", "")
                for cat in categories_raw
                if isinstance(cat, dict) and "title" in cat and cat.get("title")
            ]

    @staticmethod
    def _update_coordinates(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update coordinates from page data."""
        try:
            coordinates_raw = page_data.get("coordinates", [])
            if isinstance(coordinates_raw, list) and coordinates_raw and not (wiki_page.lat and wiki_page.lon):
                coord = coordinates_raw[0]
                if isinstance(coord, dict):
                    wiki_page.lat = float(coord.get("lat")) if coord.get("lat") is not None else None
                    wiki_page.lon = float(coord.get("lon")) if coord.get("lon") is not None else None
        except Exception as e:
            logger.warning(f"Error processing coordinates: {e}")

    @staticmethod
    def _update_internal_links(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update internal links from page data."""
        if not wiki_page.internal_links:
            links_raw = page_data.get("links", [])
            if isinstance(links_raw, list):
                wiki_page.internal_links = [
                    link["title"]
                    for link in links_raw
                    if isinstance(link, dict) and "title" in link and link.get("title")
                ]

    @staticmethod
    def _update_thumbnail(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update thumbnail URL from page data."""
        thumbnail_raw = page_data.get("thumbnail", {})
        if isinstance(thumbnail_raw, dict) and not wiki_page.thumbnail_url:
            wiki_page.thumbnail_url = thumbnail_raw.get("source")

    @staticmethod
    def _update_infobox_type(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update infobox type from page data."""
        if not wiki_page.infobox_type:
            pageprops = page_data.get("pageprops", {})
            if isinstance(pageprops, dict):
                ib_list = pageprops.get("infoboxes")
                if isinstance(ib_list, list) and ib_list:
                    wiki_page.infobox_type = ib_list[0]

    @staticmethod
    def _update_langlinks(wiki_page: WikiPage, page_data: dict[str, Any]) -> None:
        """Update language links from page data."""
        langlinks = page_data.get("langlinks", [])
        if isinstance(langlinks, list):
            for link in langlinks:
                if isinstance(link, dict) and "lang" in link and "title" in link:
                    if link["lang"] == "en" and not wiki_page.title_en:
                        wiki_page.title_en = link["title"]
                        # Generate English URL
                        if not wiki_page.wiki_url_en or wiki_page.wiki_url_en == "":
                            wiki_page.wiki_url_en = f"https://en.wikipedia.org/wiki/{link['title'].replace(' ', '_')}"
                    elif link["lang"] == "de" and not wiki_page.title_de:
                        wiki_page.title_de = link["title"]
                        # Generate German URL
                        if not wiki_page.wiki_url_de or wiki_page.wiki_url_de == "":
                            wiki_page.wiki_url_de = f"https://de.wikipedia.org/wiki/{link['title'].replace(' ', '_')}"

    @staticmethod
    def _update_urls(wiki_page: WikiPage, lang: str) -> None:
        """Generate Wikipedia URLs based on titles."""
        if lang == "de" and wiki_page.title_de and (not wiki_page.wiki_url_de or wiki_page.wiki_url_de == ""):
            wiki_page.wiki_url_de = f"https://de.wikipedia.org/wiki/{wiki_page.title_de.replace(' ', '_')}"
        elif lang == "en" and wiki_page.title_en and (not wiki_page.wiki_url_en or wiki_page.wiki_url_en == ""):
            wiki_page.wiki_url_en = f"https://en.wikipedia.org/wiki/{wiki_page.title_en.replace(' ', '_')}"

    @staticmethod
    def generate_dbpedia_uri(title_en: str) -> str:
        """
        Generate DBpedia URI from English Wikipedia title.

        Args:
            title_en: English Wikipedia page title

        Returns:
            DBpedia URI string
        """
        if not title_en or not title_en.strip():
            return ""

        # Clean and format the title for DBpedia
        # Replace spaces with underscores and encode special characters
        dbpedia_title = title_en.strip().replace(" ", "_")

        # DBpedia resource URI format
        dbpedia_uri = f"http://dbpedia.org/resource/{dbpedia_title}"

        logger.debug(f"Generated DBpedia URI: {dbpedia_uri} from title: {title_en}")
        return dbpedia_uri

    @staticmethod
    def format_wiki_page(page: WikiPage) -> dict[str, Any]:
        """Format a WikiPage object into the expected output format."""
        logger.debug(f"Formatting WikiPage: title_de='{page.title_de}', title_en='{page.title_en}'")

        result = {
            "status": "found",  # Indicate successful Wikipedia linking
            "label_de": page.title_de or "",
            "label_en": page.title_en or "",
            "url_de": page.wiki_url_de or "",
            "url_en": page.wiki_url_en or "",
            "extract": page.abstract_de or page.abstract_en or "",  # Prioritize German, fallback to English
            "wikidata_id": page.wikidata_id or "",
            "thumbnail_url": page.thumbnail_url or "",
            "categories": page.categories or [],
            "internal_links": page.internal_links or [],
            "geo_lat": page.lat,
            "geo_lon": page.lon,
            "infobox_type": page.infobox_type or "",
            "dbpedia_uri": "",  # Will be generated later in finalize_dbpedia_uri
        }

        logger.debug(f"Formatted result extract field: '{result['extract'][:100] if result['extract'] else 'EMPTY'}...")
        return result

    @staticmethod
    def create_empty_wikipedia_data(label: str, status: str, error: str | None = None) -> dict[str, Any]:
        """Create empty Wikipedia data structure for failed lookups."""
        data = {
            "label_de": label,  # Use provided label as German fallback
            "label_en": "",  # No English label available
            "url_de": "",  # No German URL available
            "url_en": "",  # No English URL available
            "extract": "",  # No extract available
            "wikidata_id": "",
            "thumbnail_url": "",
            "categories": [],
            "internal_links": [],
            "lat": None,
            "lon": None,
            "infobox_type": "",
            "dbpedia_uri": "",  # No DBpedia URI available
            "status": status,
        }

        if error:
            data["error"] = error

        return data

    @staticmethod
    def enhance_with_prompt_data(wikipedia_data: dict[str, Any], prompt_metadata: dict[str, Any]) -> dict[str, Any]:
        """
        Enhance Wikipedia data with prompt-provided fallback data.

        Args:
            wikipedia_data: Current Wikipedia data
            prompt_metadata: Metadata from entity extraction prompts

        Returns:
            Enhanced Wikipedia data with fallbacks
        """
        # Extract prompt data
        prompt_label_de = prompt_metadata.get("label_de", "")
        prompt_label_en = prompt_metadata.get("label_en", "")
        prompt_url_de = prompt_metadata.get("wiki_url_de", "")
        prompt_url_en = prompt_metadata.get("wiki_url_en", "")

        # Use prompt data as fallback for empty fields
        if not wikipedia_data.get("label_de") and prompt_label_de:
            wikipedia_data["label_de"] = prompt_label_de
            logger.debug(f"Enhanced with prompt label_de: {prompt_label_de}")

        if not wikipedia_data.get("label_en") and prompt_label_en:
            wikipedia_data["label_en"] = prompt_label_en
            logger.debug(f"Enhanced with prompt label_en: {prompt_label_en}")

        if not wikipedia_data.get("url_de") and prompt_url_de:
            wikipedia_data["url_de"] = prompt_url_de
            logger.debug(f"Enhanced with prompt url_de: {prompt_url_de}")

        if not wikipedia_data.get("url_en") and prompt_url_en:
            wikipedia_data["url_en"] = prompt_url_en
            logger.debug(f"Enhanced with prompt url_en: {prompt_url_en}")

        return wikipedia_data

    @staticmethod
    def finalize_dbpedia_uri(wikipedia_data: dict[str, Any]) -> dict[str, Any]:
        """
        Generate final DBpedia URI using the best available English data.

        This should be called at the end of processing after all fallbacks.

        Args:
            wikipedia_data: Wikipedia data with all enhancements

        Returns:
            Wikipedia data with finalized DBpedia URI
        """
        # Priority order for DBpedia URI generation:
        # 1. Use existing DBpedia URI if it's valid and non-empty
        # 2. Generate from label_en (from Wikipedia or prompt)
        # 3. Extract from url_en (from Wikipedia or prompt)

        current_dbpedia_uri = wikipedia_data.get("dbpedia_uri", "")
        if current_dbpedia_uri and current_dbpedia_uri.strip() and current_dbpedia_uri != "":
            logger.debug(f"Using existing DBpedia URI: {current_dbpedia_uri}")
            return wikipedia_data

        # Try to generate from label_en
        label_en = wikipedia_data.get("label_en", "")
        if label_en and label_en.strip():
            dbpedia_uri = WikipediaDataProcessor.generate_dbpedia_uri(label_en)
            if dbpedia_uri:
                wikipedia_data["dbpedia_uri"] = dbpedia_uri
                logger.debug(f"Generated final DBpedia URI from label_en '{label_en}': {dbpedia_uri}")
                return wikipedia_data

        # Try to extract from url_en
        url_en = wikipedia_data.get("url_en", "")
        if url_en and "en.wikipedia.org/wiki/" in url_en:
            url_title = url_en.split("en.wikipedia.org/wiki/")[-1]
            # Replace underscores with spaces for proper title
            title_from_url = url_title.replace("_", " ")
            dbpedia_uri = WikipediaDataProcessor.generate_dbpedia_uri(title_from_url)
            if dbpedia_uri:
                wikipedia_data["dbpedia_uri"] = dbpedia_uri
                logger.debug(f"Generated final DBpedia URI from url_en '{url_en}': {dbpedia_uri}")
                return wikipedia_data

        # No English data available - keep empty URI
        wikipedia_data["dbpedia_uri"] = ""
        logger.debug("No English data available for DBpedia URI generation")
        return wikipedia_data
