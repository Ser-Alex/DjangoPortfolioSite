from django.contrib import admin

from portfolio.models import HistoryWedding, HistoryImage


class HistoryInlineImages(admin.TabularInline):
    model = HistoryImage
    extra = 0


@admin.register(HistoryWedding)
class AdminBannerCategory(admin.ModelAdmin):
    list_display = ['title', 'intro', 'active']
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


