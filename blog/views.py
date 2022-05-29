from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import PostSerializer
from .models import Post


class LatestPostsList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()[:8]
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostsList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetail(APIView):
    def get_object(self, post_slug):
        try:
            return Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_slug, format=None):
        post = self.get_object(post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    if query := request.data.get('query', ''):
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    else:
        return Response({"posts": []})
