from django.db.models import Sum
from rest_framework import serializers

from .models import Story, Category, Chapter

from user.serializers import UserStorySerializer
from action.serializers import CommentSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class StorySerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    follow = serializers.SerializerMethodField(read_only=True)
    view = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField()

    category = CategorySerializer(many=True)
    author = UserStorySerializer()

    def get_view(self, obj):
        return obj.view.count()

    def get_comment(self, obj):
        return obj.comment.count()

    def get_avatar(self, obj):
        request = self.context['request']
        name = obj.avatar.name
        path = '/static/%s' % name
        return request.build_absolute_uri(path)

    def get_rating(self, obj):
        try:
            rate__sum = obj.rating.aggregate(Sum('rate'))
            sum_rate = rate__sum['rate__sum']
            number_rate = obj.rating.count()
            ratio = sum_rate/number_rate
            return {
                'rate': ratio,
                'number': number_rate,
            }
        except Exception:
            return {
                'rate': 0,
                'number': 0,
            }

    def get_follow(self, obj):
        return obj.follow.count()

    class Meta:
        model = Story
        fields = ['id', 'name', 'avatar', 'author', 'rating', 'introduce', 'status', 'category', 'follow', 'comment', 'view']


class StoryTopSerializer(serializers.ModelSerializer):
    sum_chap = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField()

    def get_sum_chap(self, obj):
        return obj.chapter.count()

    def get_avatar(self, obj):
        request = self.context['request']
        name = obj.avatar.name
        path = '/static/%s' % name
        return request.build_absolute_uri(path)

    class Meta:
        model = Story
        fields = ['id', 'name', 'avatar', 'status', 'sum_chap']


class StoryUpdateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    new_chap = serializers.SerializerMethodField(read_only=True)

    def get_new_chap(self, obj):
        chap = obj.chapter.filter(active=True).order_by('-updated_date')[:1]
        return ChapterBaseSerializer(chap, many=True).data

    class Meta:
        model = Story
        fields = ['id', 'name', 'category', 'status', 'new_chap']

class StorySmallSerializer(serializers.ModelSerializer):
    sum_chap = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(many=True)

    def get_sum_chap(self, obj):
        return obj.chapter.count()

    class Meta:
        model = Story
        fields = ['id', 'name', 'avatar', 'category', 'sum_chap']

class ChapterSerializer(serializers.ModelSerializer):
    story = StorySmallSerializer()

    class Meta:
        model = Chapter
        exclude = ['active', 'updated_date']

class ChapterCommentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ['id', 'number', 'comment']

class ChapterBaseSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()

    def get_view(self, obj):
        return obj.view.count()

    class Meta:
        model = Chapter
        fields = ['id', 'number', 'name', 'view', 'updated_date']



