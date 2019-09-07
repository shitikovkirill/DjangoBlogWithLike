from apps.accounts.serializers import UserSerializer
from rest_framework import serializers
from apps.blog.models import Post, Like


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("like", "user")


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "description", "user", "is_liked")

    def get_is_liked(self, obj) -> bool:
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        like = Like.objects.filter(user=user, post=obj).first()
        return bool(like)
