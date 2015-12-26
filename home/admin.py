from django.contrib import admin

from .models import Box, Quote


class BoxAdmin(admin.ModelAdmin):
    ordering = ('sort_order',)

admin.site.register(Box, BoxAdmin)
admin.site.register(Quote)
