"""
Management command to clean up character-related data in the database.

This includes:
- Deleting characters missing required fields (name, image, or quirks)
- Removing junk or malformed aliases
- Deleting orphaned CharacterQuirk and CharacterAffiliation objects
"""

import os
from django.core.management.base import BaseCommand
from django.db import transaction
from characters.models import Character, Alias, CharacterQuirk, CharacterAffiliation


class Command(BaseCommand):
    """
    Command to perform database cleanup for character-related models.

    Supports a --dry-run flag to preview changes without committing deletions.
    """

    help = "Remove incomplete characters, junk aliases, and orphaned related data."

    def add_arguments(self, parser):
        """
        Adds optional command-line arguments for this command.

        --dry-run: If specified, only outputs which deletions would occur.
        """
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without deleting data.",
        )

    def handle(self, *args, **options):
        """
        Executes the cleanup operation.

        Deletes incomplete Character entries,
        malformed aliases, and orphaned related objects.
        If --dry-run is passed, only outputs what would be deleted.
        """
        dry_run = options["dry_run"]

        with transaction.atomic():
            # Delete characters with missing name, image, or quirks
            incomplete = (
                Character.objects.filter(image="")
                | Character.objects.filter(name="")
                | Character.objects.filter(characterquirk__isnull=True)
            )

            # Check for missing image files
            for char in Character.objects.exclude(image=""):
                if char.image and not os.path.exists(char.image.path):
                    incomplete |= Character.objects.filter(pk=char.pk)

            incomplete = incomplete.distinct()
            for char in incomplete:
                self.stdout.write(
                    f"{'[Dry Run] Would delete' if dry_run else 'Deleting'} "
                    f"incomplete character: {char.name}"
                )
                if not dry_run:
                    char.delete()

            # Delete bad aliases
            bad_aliases = Alias.objects.filter(
                name__regex=r"^[^a-zA-Z0-9]+$"
            ) | Alias.objects.filter(name__in=["(", ")", ",", "?", ""])
            count = bad_aliases.count()
            if dry_run:
                self.stdout.write(f"[Dry Run] Would delete {count} bad aliases.")
            else:
                bad_aliases.delete()
                self.stdout.write(f"Deleted {count} bad aliases.")

            # Delete orphaned related objects
            orphaned_quirks = CharacterQuirk.objects.filter(character__isnull=True)
            orphaned_affiliations = CharacterAffiliation.objects.filter(
                character__isnull=True
            )

            quirks_count = orphaned_quirks.count()
            affiliations_count = orphaned_affiliations.count()

            if dry_run:
                self.stdout.write(
                    f"[Dry Run] Would delete {quirks_count} orphaned quirk relations."
                )
                self.stdout.write(
                    f"[Dry Run] Would delete "
                    f"{affiliations_count} orphaned affiliation relations."
                )
            else:
                orphaned_quirks.delete()
                orphaned_affiliations.delete()
                self.stdout.write(f"Deleted {quirks_count} orphaned quirk relations.")
                self.stdout.write(
                    f"Deleted {affiliations_count} orphaned affiliation relations."
                )
