from django.contrib import admin

from .models import Category, Story, Chapter

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']

class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'active']
    list_filter = ['author', 'active']
    search_fields = ['name']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'story', 'active']
    list_filter = ['story', 'active']
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)

# Register your models here.
