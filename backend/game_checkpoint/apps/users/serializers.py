from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from game_checkpoint.apps.users.models import Follow
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from .models import User, Follow

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('gcrefresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'gcrefresh\'')


class ThumbnailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    image = serializers.CharField(allow_blank=True, required=False)


    class Meta:
        model = User
        fields = ['username', 'email', 'image']
        read_only_fields = ['email',]


class SessionSerializer(ThumbnailSerializer):
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['role', 'username', 'email', 'image']

class ProfileSerializer(ThumbnailSerializer):
    following = serializers.SerializerMethodField()
    comments = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'following']
    
    def get_following(self, data):
        return Follow.objects.filter(
            follower=self.context['user'], 
            following=self.context['follow']
        ).exists()
 
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
    
    def create(self):
        return Follow.objects.create(
            follower=self.context['user'], 
            following=self.context['follow']
        )

    def delete(self):
        return Follow.objects.filter(
            follower=self.context['user'], 
            following=self.context['follow']
        ).delete()
 