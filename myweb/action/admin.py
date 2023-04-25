from django.contrib import admin

from .models import Comment, Like, Rating, View, Follow, Dislike

class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'chap', 'author']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'author', 'active']

class DislikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'author', 'active']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['rate', 'story', 'author']

class FollowAdmin(admin.ModelAdmin):
    list_display = ['story', 'author']

class ViewAdmin(admin.ModelAdmin):
    list_display = ['author', 'story', 'created_date']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Follow, FollowAdmin)

# Register your models here.
