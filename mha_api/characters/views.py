from rest_framework import generics
from .models import Character
from .serializers import CharacterSerializer


class CharacterList(generics.ListAPIView):
    """
    API view that returns a list of all characters.
    """

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class CharacterDetail(generics.RetrieveAPIView):
    """
    API view that retrieves a single character by ID.
    """

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
