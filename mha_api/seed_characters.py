import os
import sys
import json
import argparse
import re
from django.conf import settings

# Add the inner 'mha_api' folder to the module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "mha_api"))

# Set Django settings module to point to the correct settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mha_api.settings")


def seed():
    import django

    django.setup()
    from characters.models import (
        Character,
        Quirk,
        Affiliation,
        CharacterQuirk,
        CharacterAffiliation,
        Alias,
    )

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Seed MHA character data.")
    parser.add_argument(
        "--reset", action="store_true", help="Delete all existing data before seeding."
    )
    args = parser.parse_args()

    if args.reset:
        print("🔄 Resetting existing data...")
        Character.objects.all().delete()
        Quirk.objects.all().delete()
        Affiliation.objects.all().delete()
        Alias.objects.all().delete()
        CharacterQuirk.objects.all().delete()
        CharacterAffiliation.objects.all().delete()

    # Load character data
    def load_jsonc(path):
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            if '"' in line or "'" in line:
                cleaned_lines.append(line)
            else:
                cleaned_lines.append(re.sub(r"//.*", "", line))

        content = "".join(cleaned_lines)
        return json.loads(content)

    data = load_jsonc("scraper/cleaned_characters.jsonc")

    for entry in data:
        name = entry["name"]
        url = entry["url"]
        kanji = entry.get("kanji", "")
        image_path = entry.get("image", "")

        char, created = Character.objects.get_or_create(
            name=name,
            defaults={
                "url": url,
                "kanji": kanji,
            },
        )

        if not created:
            char.url = url
            char.kanji = kanji
            char.save()

        if image_path:
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            if os.path.exists(full_path):
                from django.core.files import File

                with open(full_path, "rb") as img_file:
                    char.image.save(
                        os.path.basename(full_path), File(img_file), save=True
                    )

        char.aliases.all().delete()
        for alias_entry in entry.get("aliases", []):
            if isinstance(alias_entry, str):
                Alias.objects.create(name=alias_entry.strip(), character=char)
            elif isinstance(alias_entry, dict) and "name" in alias_entry and isinstance(alias_entry["name"], str):
                Alias.objects.create(name=alias_entry["name"].strip(), character=char)
            else:
                print(f"⚠️ Skipped unrecognized alias format for {char.name}: {alias_entry}")

        for idx, q in enumerate(entry.get("quirks", [])):
            quirk, _ = Quirk.objects.get_or_create(name=q["name"])
            CharacterQuirk.objects.get_or_create(
                character=char, quirk=quirk, defaults={"order": idx}
            )

        for idx, aff in enumerate(entry.get("affiliations", [])):
            affiliation, _ = Affiliation.objects.get_or_create(name=aff["name"])
            CharacterAffiliation.objects.get_or_create(
                character=char,
                affiliation=affiliation,
                defaults={
                    "note": aff.get("note", ""),
                    "order": idx,
                },
            )

    print("✅ Done seeding character data!")


if __name__ == "__main__":
    seed()
