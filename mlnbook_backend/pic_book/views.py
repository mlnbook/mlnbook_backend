# coding=utf-8
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, Chapter, Paragraph, \
    BookSeries, IllustrationFile, LayoutTemplate, BookPage
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterSerializer, LayoutTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, \
    BookSeriesCreateSerializer, BookPageSerializer, BookPageParagraphSerializer, ChapterParagraphSerializer, \
    ChapterPageSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer

    @action(detail=True)
    def chapter(self, request, pk=None):
        pic_book = self.get_object()
        chapter_queryset = pic_book.chapter_set.all()
        serializer = ChapterSerializer(chapter_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def chapter_page(self, request, pk=None):
        pic_book = self.get_object()
        chapter_queryset = pic_book.chapter_set.all()
        serializer = ChapterPageSerializer(chapter_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def chapter_page_paragraph(self, request, pk=None):
        pic_book = self.get_object()
        chapter_queryset = pic_book.chapter_set.all()
        serializer = ChapterParagraphSerializer(chapter_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def page_paragraph(self, request, pk=None):
        pic_book = self.get_object()
        page_queryset = pic_book.bookpage_set.all()
        serializer = BookPageParagraphSerializer(page_queryset, many=True)
        return Response(serializer.data)


class KnowledgePointViewSet(viewsets.ModelViewSet):
    queryset = KnowledgePoint.objects.all()
    serializer_class = KnowledgePointSerializer


class LayoutTemplateViewSet(viewsets.ModelViewSet):
    queryset = LayoutTemplate.objects.all()
    serializer_class = LayoutTemplateSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @action(detail=True)
    def page(self, request, pk=None):
        chapter = self.get_object()
        bookpage_queryset = chapter.bookpage_set.all()
        serializer = BookPageSerializer(bookpage_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def page_paragraph(self, request, pk=None):
        chapter = self.get_object()
        bookpage_queryset = chapter.bookpage_set.all()
        serializer = BookPageParagraphSerializer(bookpage_queryset, many=True)
        return Response(serializer.data)


class BookPageViewSet(viewsets.ModelViewSet):
    queryset = BookPage.objects.all()
    serializer_class = BookPageSerializer

    def get_serializer_class(self):
        if self.action in ["create", "list", "retrieve"]:
            return BookPageParagraphSerializer
        else:
            return BookPageSerializer

    @action(detail=True)
    def paragraph(self, request, pk=None):
        page = self.get_object()
        paragraph_queryset = page.paragraphs.all()
        serializer = ParagraphSerializer(paragraph_queryset, many=True)
        return Response(serializer.data)


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
