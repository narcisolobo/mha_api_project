from rest_framework import filters, generics
from .models import Character
from .serializers import CharacterSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    summary="List all characters",
    description="Retrieve a list of My Hero Academia characters. You can filter results by name using the `search` query parameter, e.g. `?search=Midoriya`.",
    examples=[
        OpenApiExample(
            name="Character List Example",
            value=[
                {
                    "id": 1,
                    "name": "Izuku Midoriya",
                    "kanji": "緑谷出久",
                    "url": "https://myheroacademia.fandom.com/wiki/Izuku_Midoriya",
                    "image": "http://localhost:8000/media/characters/izuku-midoriya_u8fpXbE.png",
                    "quirks": [
                        {"name": "Quirkless"},
                        {"name": "One For All"},
                        {"name": "Gearshift"},
                        {"name": "Fa Jin"},
                        {"name": "Danger Sense"},
                        {"name": "Blackwhip"},
                        {"name": "Smokescreen"},
                        {"name": "Float"},
                    ],
                    "affiliations": [
                        {"name": "Aldera Junior High", "note": "Formerly"},
                        {"name": "U.A. High School", "note": ""},
                    ],
                    "aliases": [{"name": "Deku"}],
                },
                {
                    "id": 148,
                    "name": "Katsuki Bakugo",
                    "kanji": "爆豪勝己",
                    "url": "https://myheroacademia.fandom.com/wiki/Dynamight",
                    "image": "http://localhost:8000/media/characters/katsuki-bakugo_U02fniw.png",
                    "quirks": [{"name": "Explosion"}, {"name": "One For All"}],
                    "affiliations": [
                        {"name": "Aldera Junior High", "note": "Formerly"},
                        {"name": "U.A. High School", "note": "Formerly"},
                        {"name": "Endeavor Agency", "note": "Formerly"},
                        {"name": "Genius Office", "note": "Formerly"},
                    ],
                    "aliases": [
                        {"name": "Kacchan"},
                        {"name": "Katchan"},
                        {
                            "name": "Explosive Hero: Great Explosion Murder God Dynamight"
                        },
                    ],
                },
                {
                    "id": 2,
                    "name": "Shoto Todoroki",
                    "kanji": "轟焦凍",
                    "url": "https://myheroacademia.fandom.com/wiki/Shoto_Todoroki",
                    "image": "http://localhost:8000/media/characters/shoto-todoroki_PPR4jCS.png",
                    "quirks": [{"name": "Half-Cold Half-Hot"}],
                    "affiliations": [
                        {"name": "Corusan Middle School", "note": "Formerly"},
                        {"name": "U.A. High School", "note": "Formerly"},
                    ],
                    "aliases": [{"name": "AirCon Hero: Shoto"}],
                },
            ],
            response_only=True,
        )
    ],
)
class CharacterList(generics.ListAPIView):
    """
    API view that returns a list of all characters.
    Supports searching by character name.
    """

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


@extend_schema(
    summary="Retrieve a character by ID",
    description="""Fetch detailed information for a single character, including quirks, affiliations, and aliases.""",
    examples=[
        OpenApiExample(
            name="Character Detail Example",
            value={
                "id": 1,
                "name": "Izuku Midoriya",
                "kanji": "緑谷出久",
                "url": "https://myheroacademia.fandom.com/wiki/Izuku_Midoriya",
                "image": "http://localhost:8000/media/characters/izuku-midoriya_u8fpXbE.png",
                "quirks": [
                    {"name": "Quirkless"},
                    {"name": "One For All"},
                    {"name": "Gearshift"},
                    {"name": "Fa Jin"},
                    {"name": "Danger Sense"},
                    {"name": "Blackwhip"},
                    {"name": "Smokescreen"},
                    {"name": "Float"},
                ],
                "affiliations": [
                    {"name": "Aldera Junior High", "note": "Formerly"},
                    {"name": "U.A. High School", "note": ""},
                ],
                "aliases": [{"name": "Deku"}],
            },
            response_only=True,
        )
    ],
)
class CharacterDetail(generics.RetrieveAPIView):
    """
    API view that retrieves a single character by ID.
    """

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
