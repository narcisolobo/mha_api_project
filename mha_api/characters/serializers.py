from rest_framework import serializers
from .models import Character, CharacterAffiliation, Quirk, Affiliation, Alias


class QuirkSerializer(serializers.ModelSerializer):
    """
    Serializer for Quirk model, returns only the name.
    """

    class Meta:
        model = Quirk
        fields = ["name"]


class AffiliationSerializer(serializers.ModelSerializer):
    """
    Serializer for Affiliation model, includes name and note.
    """

    class Meta:
        model = Affiliation
        fields = ["name", "note"]


class AliasSerializer(serializers.ModelSerializer):
    """
    Serializer for Alias model, includes only the name.
    """

    class Meta:
        model = Alias
        fields = ["name"]


class CharacterAffiliationSerializer(serializers.ModelSerializer):
    """
    Serializer for the CharacterAffiliation model, flattening name and note.
    """

    name = serializers.CharField(source="affiliation.name")

    class Meta:
        model = CharacterAffiliation
        fields = ["name", "note"]


class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializer for Character model, returning nested quirks, affiliations, and aliases.
    Includes an image and kanji field.
    """

    quirks = serializers.SerializerMethodField()
    affiliations = CharacterAffiliationSerializer(
        source="characteraffiliation_set", many=True, read_only=True
    )
    aliases = AliasSerializer(many=True, read_only=True)
    image = serializers.ImageField()

    def get_quirks(self, obj):
        queryset = obj.characterquirk_set.all().order_by("order")
        return QuirkSerializer([cq.quirk for cq in queryset], many=True).data

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "kanji",
            "url",
            "image",
            "quirks",
            "affiliations",
            "aliases",
        ]
