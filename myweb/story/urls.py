from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet, 'category')
router.register('story', views.StoryViewSet, 'story')
router.register('chapter', views.ChapterViewSet, 'chapter')

urlpatterns = [
    path('', include(router.urls)),
]