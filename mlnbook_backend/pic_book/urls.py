# coding=utf-8
from django.urls import path, include, re_path
from rest_framework import routers

from mlnbook_backend.pic_book.views import PicBookViewSet, KnowledgePointViewSet, LayoutTemplateViewSet, \
    ParagraphViewSet, BookSeriesViewSet, ChapterViewSet, BookPageViewSet, \
    VoiceTemplateViewSet, AuthorViewSet, ParagraphVoiceFileViewSet, PicBookVoiceViewSet

router = routers.DefaultRouter()
router.register('book', PicBookViewSet)
router.register('knowledge', KnowledgePointViewSet)
router.register('chapter', ChapterViewSet)
router.register('layout', LayoutTemplateViewSet)
router.register('paragraph', ParagraphViewSet)
router.register('book_page', BookPageViewSet)
router.register('book_series', BookSeriesViewSet)
router.register('voice_template', VoiceTemplateViewSet)
router.register('book_voice', PicBookVoiceViewSet)
router.register('paragraph_voice', ParagraphVoiceFileViewSet)
router.register('author', AuthorViewSet)

# router.register('pic_upload', IllustrationFileUploadView)
# urlpatterns = [
#     # re_path(r'^pic_upload/(?P<filename>[^/]+)$', IllustrationFileUploadView.as_view())
# ]
#
urlpatterns = router.urls
