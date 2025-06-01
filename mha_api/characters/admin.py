from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import (
    Affiliation,
    Alias,
    Character,
    CharacterAffiliation,
    CharacterQuirk,
    Quirk,
)


class AliasInline(admin.TabularInline):
    """Inline admin interface for editing Alias instances related to a Character."""

    model = Alias
    extra = 1


class CharacterQuirkInline(admin.TabularInline):
    """
    Inline admin interface for editing
    CharacterQuirk instances related to a Character.
    """

    model = CharacterQuirk
    extra = 1
    autocomplete_fields = ["quirk"]
    ordering = ["order"]
    fields = ["quirk", "order"]


class CharacterAffiliationInline(admin.TabularInline):
    """
    Inline admin interface for editing
    CharacterAffiliation instances related to a Character.
    """

    model = CharacterAffiliation
    extra = 0
    autocomplete_fields = ["affiliation"]
    ordering = ["order"]
    fields = ["affiliation", "note", "order"]


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    """Admin interface customization class for Affiliation model."""

    search_fields = ("name",)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Admin interface customization class for Character model."""

    inlines = [AliasInline, CharacterQuirkInline, CharacterAffiliationInline]
    list_display = ("name", "kanji", "image_preview")
    readonly_fields = ("image_preview",)
    fields = ("name", "kanji", "url", "image_preview", "image")
    search_fields = ("name", "kanji")

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "(No image)"

    image_preview.short_description = "Image Preview"


@admin.register(CharacterAffiliation)
class CharacterAffiliationAdmin(admin.ModelAdmin):
    """Admin interface customization class for CharacterAffiliation model."""

    pass


@admin.register(CharacterQuirk)
class CharacterQuirkAdmin(admin.ModelAdmin):
    """Admin interface customization class for CharacterQuirk model."""

    pass


@admin.register(Quirk)
class QuirkAdmin(admin.ModelAdmin):
    """Admin interface customization class for Quirk model."""

    search_fields = ("name",)
