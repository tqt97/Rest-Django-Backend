from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'get_absolute_url', 'description', 'body', 'slug', 'image',
                  'get_image', 'get_thumbnail', 'created_at', 'updated_at', 'get_description','get_title')
