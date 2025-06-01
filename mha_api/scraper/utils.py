"""
Utility functions used by the MHA character scraper. Includes functions for
parsing quirks, affiliations, aliases, and downloading images.
"""

import os
import requests
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
MEDIA_DIR = os.path.join(PROJECT_ROOT, "mha_api", "media", "characters")


def extract_quirks(value):
    """
    Extracts quirk names and optional notes from a raw text value.

    Args:
        value (str): The raw string from the 'quirk' field in the infobox.

    Returns:
        list[dict]: List of quirks with 'name' and optional 'note'.
    """
    parts = re.findall(r"([\w\s\-]+)(?:\s*\(([^)]+)\))?", value)
    quirks = []
    for name, note in parts:
        name = name.strip()
        if not name:
            continue
        entry = {"name": name}
        if note and note.lower() != name.lower():
            entry["note"] = note.strip()
        quirks.append(entry)
    return quirks


def parse_affiliations(raw):
    """
    Parses and cleans the affiliations from the infobox raw text value.

    Args:
        raw (str): The raw affiliation string from the infobox.

    Returns:
        list[dict]: List of affiliation objects with 'name' and optional 'note'.
    """
    ascii_only = re.sub(r"[^\x00-\x7F]+", "", raw)
    no_footnotes = re.sub(r"\[\s*\|?\s*\d+\s*\|?\s*\]", "", ascii_only)
    standardized = re.sub(r"\s*\|\s*", "|", no_footnotes)
    cleaned = re.sub(r"\s+", " ", standardized).strip()
    parts = [
        p.strip()
        for p in cleaned.split("|")
        if p.strip() and p not in {"(", ")", ",", "?"}
    ]

    affiliations = []
    i = 0
    while i < len(parts):
        name = parts[i]
        note = None
        if i + 1 < len(parts) and parts[i + 1].lower() == "(formerly)":
            note = "Formerly"
            i += 1
        affiliations.append({"name": name, **({"note": note} if note else {})})
        i += 1

    for aff in affiliations:
        if aff["name"] == "Korusan Chgakk":
            aff["name"] = "Corusan Middle School"

    return affiliations


def dedupe_affiliations(affiliations):
    """
    Removes duplicate affiliations, prioritizing entries with notes when available.

    Args:
        affiliations (list[dict]): A list of affiliation dicts.

    Returns:
        list[dict]: Deduplicated list of affiliations.
    """
    seen = {}
    for aff in affiliations:
        name = aff["name"]

        if name not in seen or ("note" in aff and "note" not in seen[name]):
            seen[name] = aff
    return list(seen.values())


def download_image(url, filename, folder=MEDIA_DIR):
    """
    Downloads an image from a URL and saves it to the specified folder.

    Args:
        url (str): URL of the image to download.
        filename (str): Name to save the image as.
        folder (str): Destination folder for saving the image.

    Returns:
        str or None: Relative path to saved image or None if download failed.
    """
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(full_path, "wb") as f:
            f.write(response.content)
        return os.path.relpath(full_path, os.path.join(PROJECT_ROOT, "media"))
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None


def extract_aliases(soup):
    """
    Extracts and cleans alias names from the character infobox.

    Args:
        soup (BeautifulSoup): Parsed HTML of the character page.

    Returns:
        list[str]: List of filtered English aliases.
    """
    alias_div = soup.find("div", {"data-source": "alias"})
    if not alias_div:
        return []

    value_div = alias_div.find("div", class_="pi-data-value")
    if not value_div:
        return []

    raw_text = value_div.get_text(separator="|", strip=True)
    parts = [p.strip() for p in raw_text.split("|") if p.strip()]

    english_aliases = []
    for alias in parts:
        if re.fullmatch(r"[ -~]+", alias):
            if (
                not re.fullmatch(r"[\[\]\d]+", alias)
                and alias not in {"(", ")", ",", "?"}
                and len(alias) >= 5
                and not alias.islower()
            ):
                english_aliases.append(alias)

    seen = set()
    cleaned = []
    for alias in english_aliases:
        if alias not in seen:
            seen.add(alias)
            cleaned.append(alias)

    return cleaned
