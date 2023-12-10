# coding=utf-8
from rest_framework import viewsets

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, ChapterTemplate, Paragraph, BookSeries
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, BookSeriesCreateSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer


class KnowledgePointViewSet(viewsets.ModelViewSet):
    queryset = KnowledgePoint.objects.all()
    serializer_class = KnowledgePointSerializer


class ChapterTemplateViewSet(viewsets.ModelViewSet):
    queryset = ChapterTemplate.objects.all()
    serializer_class = ChapterTemplateSerializer


class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer


class BookSeriesViewSet(viewsets.ModelViewSet):
    queryset = BookSeries.objects.all()
    serializer_class = ParagraphSerializer

    def get_serializer_class(self):
        if self.action in ("list", "detail"):
            return BookSeriesListSerializer
        else:
            return BookSeriesCreateSerializer
