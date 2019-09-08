from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from apps.blog.access_policy import PostAccessPolicy, LikeAccessPolicy
from apps.blog.serializers import PostSerializer, LikeSerializer
from apps.blog.permissions import IsOwner
from apps.blog.models import Post, Like


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAccessPolicy]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.get_posts_include_unpablished(user)
        return self.queryset.published()

    def create(self, request):
        composition = Post.objects.create(**request.data, user=request.user)
        composition.save()
        serializer_context = {"request": request}
        serializer = PostSerializer(composition, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [LikeAccessPolicy, IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view should return a list of all the likes
        for the currently authenticated user.
        """
        params = {}
        if self.request.user.is_anonymous:
            raise NotAuthenticated("You must login for get this data!")
        params["user"] = self.request.user

        if self.request.query_params.get("composition"):
            params["composition__id"] = self.request.query_params.get("composition")

        return self.queryset.filter(**params)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.request.data["post"]["id"])
        serializer.save(user=self.request.user, post=post)
