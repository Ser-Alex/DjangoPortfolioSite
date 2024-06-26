from django.contrib import admin
from django.db.utils import ProgrammingError

from portfolio.models import HistoryWedding, HistoryImage, SiteSettings, Testimony


class HistoryInlineImages(admin.TabularInline):
    model = HistoryImage
    extra = 0


@admin.register(HistoryWedding)
class HistoryWeddingAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_intro', 'active']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HistoryInlineImages]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'intro', 'preview'),
        }),
        ('Дополнительная информация', {
            'classes': ('collapse',),
            'fields': ('active', 'preview_small', 'slug'),
        }),
    )

    def short_intro(self, obj):
        return obj.intro[:50]


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['author', 'short_text']

    def short_text(self, obj):
        return obj.text[:50]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            SiteSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False
