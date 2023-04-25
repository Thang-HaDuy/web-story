from rest_framework import serializers

from .models import Comment, Like, Rating, Follow, View

from story.models import Story

from user.serializers import UserSerializer, UserSmallSerializer


# serializer story
class StoryActionSerializer(serializers.ModelSerializer):
    sum_chap = serializers.SerializerMethodField(read_only=True)

    def get_sum_chap(self, obj):
        return obj.chapter.count()

    class Meta:
        model = Story
        fields = ['id', 'name', 'avatar', 'status', 'sum_chap']


# serializer action
class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    dislike = serializers.SerializerMethodField(read_only=True)
    child = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer()

    def get_like(self, obj):
        return obj.like.count()

    def get_dislike(self, obj):
        return obj.dislike.count()

    def get_child(self, obj):
        return obj.comment.count()

    story = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_data'
     )

    chap = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_data'
    )
    class Meta:
        model = Comment
        fields = ['content', 'author', 'like', 'dislike', 'child', 'chap', 'story', 'created_date']

class ChildCommentSerializer(serializers.ModelSerializer):
    author = UserSmallSerializer()
    class Meta:
        model = Comment
        fields = ['author', 'content', 'created_date']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['active']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['active']

class ViewSerializer(serializers.ModelSerializer):
    story = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_data'
     )

    chap = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_data'
    )

    class Meta:
        model = View
        fields = ['story', 'chap', 'created_date']

class FollowSerializer(serializers.ModelSerializer):
    story = StoryActionSerializer()

    class Meta:
        model = Follow
        fields = ['story']

