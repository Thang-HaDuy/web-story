from django.db import models

from user.models import User


class BaseStory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(BaseStory):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Story(BaseStory):
    name = models.CharField(max_length=400)
    avatar = models.ImageField(upload_to='story/images/%Y/%m/%d', null=True)
    category = models.ManyToManyField(Category, related_name='story')
    status = models.BooleanField(default=True)
    introduce = models.TextField()
    author = models.ForeignKey(User, related_name='story', on_delete=models.SET_NULL, null=True, blank=True)


    @property# SlugRelatedField
    def full_data(self):
        return {
            'id': self.pk,
            'name': self.name,
        }

    @property  # SlugRelatedField
    def data_comment(self):
        return {
            'id': self.pk,
            'name': self.name,
            'avatar': self.avatar,
        }

    def __str__(self):
        return self.name

class Chapter(BaseStory):
    name = models.CharField(max_length=400, null=True)
    story = models.ForeignKey(Story, related_name='chapter', on_delete=models.CASCADE)
    number = models.IntegerField()
    content = models.TextField()

    @property  # SlugRelatedField
    def full_data(self):
        return {
            'id': self.pk,
            'name': self.name,
        }


    def __str__(self):
        return self.name



# Create your models here.
