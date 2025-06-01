"""
Scraper for character data from the MHA wiki. Extracts key info such as name, kanji,
aliases, quirks, affiliations, and downloads images. Outputs to a JSON file.
"""

from utils import (
    dedupe_affiliations,
    download_image,
    extract_aliases,
    extract_quirks,
    parse_affiliations,
)
from bs4 import BeautifulSoup
import requests
from json import dump
from pprint import pprint
from slugify import slugify
import os
from character_urls import character_urls
import time
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
MEDIA_DIR = os.path.join(PROJECT_ROOT, "mha_api", "media", "characters")
JSON_PATH = os.path.join(PROJECT_ROOT, "mha_api", "characters.json")


def scrape_character(url):
    """
    Scrapes character data from a given MHA wiki character URL.

    Args:
        url (str): The character's wiki page URL.

    Returns:
        dict: A dictionary with extracted character data. May contain keys like
        'name', 'kanji', 'image', 'aliases', 'quirks', 'affiliations', and always 'url'.
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    infobox = soup.find("aside", class_="portable-infobox")
    if not infobox:
        print(f"No infobox found for {url}")
        return {"url": url}

    character = {"url": url}

    name_tag = infobox.find("h2", attrs={"data-source": "name"})
    if name_tag:
        character["name"] = name_tag.text.strip()

    kanji_div = infobox.select_one('[data-source="kanji"] .pi-data-value')
    if kanji_div:
        kanji_text = kanji_div.get_text(strip=True)
        kanji_clean = "".join(c for c in kanji_text if ord(c) > 127)
        if kanji_clean:
            character["kanji"] = kanji_clean

    image_anchor = infobox.select_one(".wds-tab__content.wds-is-current figure a")
    if image_anchor and image_anchor.has_attr("href"):
        character["image"] = image_anchor["href"]

    for item in infobox.find_all("div", class_="pi-data"):
        label_el = item.find(class_="pi-data-label")
        value_el = item.find(class_="pi-data-value")
        if not label_el or not value_el:
            continue

        label = label_el.text.strip().lower()
        value = value_el.get_text(separator=" | ", strip=True)
        character["aliases"] = extract_aliases(soup)

        if "quirk" in label:
            character["quirks"] = extract_quirks(value)
        elif "affiliation" in label:
            character["affiliations"] = parse_affiliations(value)

    image_el = infobox.find("figure", class_="pi-item pi-image")
    if image_el:
        img_tag = image_el.find("img")
        if img_tag and img_tag.has_attr("src"):
            image_url = img_tag["src"]
            filename = slugify(character["name"]) + ".png"
            image_path = download_image(image_url, filename)
            if image_path:
                character["image"] = f"characters/{filename}"

    character["affiliations"] = dedupe_affiliations(character.get("affiliations", []))

    return character


if __name__ == "__main__":
    urls = character_urls[208:]

    all_characters = []
    for url in urls:
        data = scrape_character(url)
        time.sleep(random.uniform(1.5, 2.5))
        if "name" not in data:
            print(f"Skipping incomplete entry: {data['url']}")
            continue
        pprint(data)
        all_characters.append(data)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        dump(all_characters, f, indent=2, ensure_ascii=False)
