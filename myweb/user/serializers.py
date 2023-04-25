from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'password', 'sex']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

class UserCurrentSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        request = self.context['request']
        name = obj.avatar.name
        path = '/static/%s' % name
        return request.build_absolute_uri(path)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'password', 'sex']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class UserStorySerializer(serializers.ModelSerializer):
    story = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='full_data'
     )
    class Meta:
        model = User
        fields = ['id', 'username', 'story']

class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']