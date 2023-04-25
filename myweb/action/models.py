from django.db import models

from user.models import User
from story.models import Story, Chapter


class BaseStory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Comment(BaseStory):
    author = models.ForeignKey(User, related_name='comment', on_delete=models.SET_NULL, null=True)
    chap = models.ForeignKey(Chapter, related_name='comment', on_delete=models.SET_NULL, blank=True, null=True)
    story = models.ForeignKey(Story, related_name='comment', on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey('Comment', related_name='comment', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if self.chap is not None:
            self.story = self.chap.story
        super().save(*args, **kwargs)


class Like(BaseStory):
    author = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='like', on_delete=models.SET_NULL, null=True)
    select = models.BooleanField(default=False)

class Dislike(BaseStory):
    author = models.ForeignKey(User, related_name='dislike', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='dislike', on_delete=models.SET_NULL, null=True)
    select = models.BooleanField(default=False)


class Rating(BaseStory):
    author = models.ForeignKey(User, related_name='rating', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='rating', on_delete=models.SET_NULL, null=True)
    rate = models.FloatField(default=0)

class Follow(BaseStory):
    author = models.ForeignKey(User, related_name='follow', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='follow', on_delete=models.SET_NULL, null=True)

class View(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='view', on_delete=models.SET_NULL, null=True, blank=True)
    story = models.ForeignKey(Story, related_name='view', on_delete=models.CASCADE, blank=True)
    chap = models.ForeignKey(Chapter, related_name='view', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.story = self.chap.story
        super().save(*args, **kwargs)






# Create your models here.
