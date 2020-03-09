from rest_framework import serializers
from .models import News,NewsCategory,Comment
from apps.qfauth.serializers import UserSerializers

class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','category','author')


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = NewsCategory
        fields = ('id','name')


