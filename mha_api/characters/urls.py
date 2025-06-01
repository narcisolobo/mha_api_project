from django.urls import path
from .views import CharacterList, CharacterDetail

urlpatterns = [
    path("characters/", CharacterList.as_view(), name="character-list"),
    path("characters/<int:pk>/", CharacterDetail.as_view(), name="character-detail"),
]
