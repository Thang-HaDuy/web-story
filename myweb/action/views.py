from rest_framework.decorators import action
from rest_framework import (
    status,
    generics,
    viewsets,
    permissions
)
from rest_framework.response import Response

from .models import Like, Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['add_like', 'delete_comment', 'add_child_comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='child-comment')
    def get_child_comment(self, request, pk):
        comment = self.get_object().comment.filter(active=True)

        return Response(CommentSerializer(comment, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add-like')
    def add_like(self, request, pk):
        try:
            author = request.user
            comment = self.get_object()
            l, _ = Like.objects.get_or_create(comment=comment, author=author)
            l.select = not l.select
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        l.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-child-comment')
    def add_child_comment(self, request, pk):
        try:
            author = request.user
            parent = self.get_object()
            c = Comment(author=author, parent=parent)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        c.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, url_path='delete-comment')
    def delete_comment(self, request, pk):
        try:
            author = request.user
            comment = self.get_object()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if comment.author == author:
            comment.delete()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)





# Create your views here.
