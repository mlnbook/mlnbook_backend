# coding=utf-8
from rest_framework import viewsets, status
# from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, Chapter, Paragraph, \
    BookSeries, IllustrationFile, LayoutTemplate, BookPage
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterSerializer, LayoutTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, \
    BookSeriesCreateSerializer, BookPageSerializer, BookPageParagraphSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer


class KnowledgePointViewSet(viewsets.ModelViewSet):
    queryset = KnowledgePoint.objects.all()
    serializer_class = KnowledgePointSerializer


class LayoutTemplateViewSet(viewsets.ModelViewSet):
    queryset = LayoutTemplate.objects.all()
    serializer_class = LayoutTemplateSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class BookPageViewSet(viewsets.ModelViewSet):
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer

    def get_serializer_class(self):
        if self.action in ["create", "list", "retrieve"]:
            return BookPageParagraphSerializer
        else:
            return BookPageSerializer


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


class IllustrationFileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        pic_file = request.data['file']
        IllustrationFile(pic_file=pic_file, user=request.user)
        return Response(status=204)
