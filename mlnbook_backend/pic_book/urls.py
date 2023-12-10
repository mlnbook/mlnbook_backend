# coding=utf-8
from django.urls import path, include
from rest_framework import routers

from mlnbook_backend.pic_book.views import PicBookViewSet, KnowledgePointViewSet, ChapterTemplateViewSet, \
    ParagraphViewSet, BookSeriesViewSet

router = routers.DefaultRouter()
router.register('pic_book', PicBookViewSet)
router.register('knowledge', KnowledgePointViewSet)
router.register('chapter', ChapterTemplateViewSet)
router.register('chapter', ChapterTemplateViewSet)
router.register('paragraph', ParagraphViewSet)
router.register('book_series', BookSeriesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = router.urls
