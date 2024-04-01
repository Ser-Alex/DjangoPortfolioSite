from django.contrib import admin

from portfolio.models import HistoryWedding


@admin.register(HistoryWedding)
class AdminBannerCategory(admin.ModelAdmin):
    list_display = ['title', 'intro', 'active']
    fields = ["title", 'intro', 'preview', 'active']


