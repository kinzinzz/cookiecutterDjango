from . import models
from djangogram.users.models import User as user_model
from rest_framework import serializers

# models에서  서로 다른 클래스라면 각각  serializer를 만들어야한다. 쿼리셋 데이터를 파이썬 데이터로 만들어준다.


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "contents",
        )


class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "profile_photo",
        )


class PostSerializer(serializers.ModelSerializer):

    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()  # 다른 모델의 serializer를 연결 => fields로 보내 알아서 만들어 준다.

    class Meta:
        model = models.Post
        fields = (
            "id",
            "image",
            "caption",
            "comment_post",
            "author",  # models에서  related_name 으로
        )
