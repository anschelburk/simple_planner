from django.contrib import admin

from .models import Event, ListItem

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end')
    search_fields = ('title',)
    list_filter = ('start', 'end')
    ordering = ('start',)

@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ('content',)
    search_fields = ('content',)