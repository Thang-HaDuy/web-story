from django.db.models import Sum, Count
from rest_framework import (
    status,
    generics,
    viewsets,
    permissions
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Story, Category, Chapter
from .paginators import (
    StoryPaginator,
    SearchPaginator,
    ChapterPaginator,
    CommentPaginator
)
from .serializers import (
    CategorySerializer,
    StorySerializer,
    ChapterSerializer,
    StoryTopSerializer,
    StoryUpdateSerializer,
    ChapterBaseSerializer,
    StorySmallSerializer,
)
from action.models import (
    Comment,
    Rating,
    Like,
    Follow,
    View
)
from action.serializers import (
    ViewSerializer,
    FollowSerializer,
    CommentSerializer
)

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=True, url_path='category-story')
    def get_story(self, request, pk):
        storys = self.get_object().story.filter(active=True)

        return Response(StorySerializer(storys, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

class StoryViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Story.objects.filter(active=True)
    serializer_class = StorySerializer
    pagination_class = StoryPaginator


    def get_permissions(self):
        if self.action in ['add_like', 'add_rating', 'add_follow']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    @action(methods=['get'], detail=False, url_path='search')
    def get_search(self, request):
        try:
            self.pagination_class = SearchPaginator
            param = request.query_params.get('q')
            types = request.query_params.get('type')
            story = self.filter_queryset(self.get_queryset()).order_by('-chapter').filter(name__icontains=param)[:5]
            if types == 'more':
                story = self.filter_queryset(self.get_queryset()).order_by('-chapter').filter(name__icontains=param)

            page = self.paginate_queryset(story)
            return self.get_paginated_response(StorySmallSerializer(page, many=True).data)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='hot-story-all')
    def get_hot_story_all(self, request):
        story = Story.objects.filter(active=True) \
                    .annotate(view_total=Count('view')) \
                    .order_by('-view_total')[:10]
        # .annotate tính tổng số lượng view
        return Response(StoryTopSerializer(story, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='hot-story-day')
    def get_hot_story_day(self, request):
        type = request.query_params.get('type')
        if type == 'slide':
            story = Story.objects.filter(active=True,
                                         view__created_date__date=timezone.now().date() - timezone.timedelta(days=1)) \
                        .annotate(view_total=Count('view')) \
                        .order_by('-view_total')[:14]
        else:
            story = Story.objects.filter(active=True, view__created_date__date=timezone.now().date() - timezone.timedelta(days=1)) \
                    .annotate(view_total=Count('view')) \
                    .order_by('-view_total')[:14]

                # .annotate tính tổng số lượng view
        return Response(StoryTopSerializer(story, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='hot-story-month')
    def get_hot_story_month(self, request):
        story = Story.objects.filter(active=True,
                                     view__created_date__date__lt=timezone.now().date(),
                                     view__created_date__date__gt=timezone.now().date() - timezone.timedelta(days=31)) \
                    .annotate(view_total=Count('view')) \
                    .order_by('-view_total')[:10]
        # .annotate tính tổng số lượng view
        return Response(StoryTopSerializer(story, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='update-story')
    def get_update_story(self, request):
        storys = Story.objects.filter(active=True).distinct("chapter").order_by('-chapter')[:35]

        return Response(StoryUpdateSerializer(storys, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='story-full')
    def get_story_full(self, request):
        storys = Story.objects.filter(status=False)[:21]

        return Response(StoryTopSerializer(storys, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='chapter')
    def get_chapter(self, request, pk):
        self.pagination_class = ChapterPaginator
        chap = self.get_object().chapter.filter(active=True).order_by('-created_date')
        page = self.paginate_queryset(chap)

        return self.get_paginated_response(ChapterBaseSerializer(page, many=True).data)

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, pk):
        self.pagination_class = CommentPaginator
        comment = self.get_object().comment.filter(active=True).order_by('-created_date')
        page = self.paginate_queryset(comment)

        return self.get_paginated_response(CommentSerializer(page, many=True).data)

    @action(methods=['post'], detail=True, url_path='add-rating')
    def add_rating(self, request, pk):
        try:
            author = request.user
            story = self.get_object()
            r, _ = Rating.objects.get_or_create(story=story, author=author)
            r.rate = float(request.data.get('rate'))
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        r.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-follow')
    def add_follow(self, request, pk):
        try:
            author = request.user
            story = self.get_object()
            f, _ = Follow.objects.get_or_create(story=story, author=author)
            f.active = not f.active
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        f.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        try:
            author = request.user
            story = self.get_object()
            content = request.data.get('content')
            c = Comment(author=author, story=story, content=content)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        c.save()
        return Response(status=status.HTTP_201_CREATED)


class ChapterViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Chapter.objects.filter(active=True)
    serializer_class = ChapterSerializer


    def get_permissions(self):
        if self.action in ['add_comment', 'delete_comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='comment')
    def get_comment(self, request, pk):
        comment = self.get_object().comment.filter(active=True).order_by('-created_date')

        return Response(CommentSerializer(comment, many=True, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        try:
            author = request.user
            chap = self.get_object()
            content = request.data.get('content')
            c = Comment(author=author, chap=chap, content=content)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        c.save()
        return Response(status=status.HTTP_200_OK)


    @action(methods=['post'], detail=True, url_path='add-view')
    def add_view(self, request, pk):
        try:
            chap = self.get_object()
            author = request.user
            v = View(chap=chap, author=author)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        v.save()
        return Response(status=status.HTTP_201_CREATED)








# Create your views here.

# timezone.now().date() - timezone.timedelta(days=1)