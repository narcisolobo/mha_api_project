from django.db import models


class Quirk(models.Model):
    """
    Represents a unique Quirk in the My Hero Academia universe.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Affiliation(models.Model):
    """
    Represents a group or organization a character can be affiliated with.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    """
    Represents a character with optional kanji name, image, URL,
    and many-to-many relationships to quirks and affiliations.
    """

    name = models.CharField(max_length=100)
    kanji = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="characters/", blank=True)

    quirks = models.ManyToManyField(Quirk, through="CharacterQuirk")
    affiliations = models.ManyToManyField(Affiliation, through="CharacterAffiliation")

    def __str__(self):
        return self.name


class CharacterQuirk(models.Model):
    """
    Intermediate model linking a Character to a Quirk with ordering.
    """

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    quirk = models.ForeignKey(Quirk, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.character} / {self.quirk}"


class CharacterAffiliation(models.Model):
    """
    Intermediate model linking a Character to
    an Affiliation with an optional note and ordering.
    """

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE)
    note = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.character} / {self.affiliation}"


class Alias(models.Model):
    """
    Represents an alternate name or alias for a character.
    """

    name = models.CharField(max_length=200)
    character = models.ForeignKey(
        "Character", on_delete=models.CASCADE, related_name="aliases"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Aliases"
