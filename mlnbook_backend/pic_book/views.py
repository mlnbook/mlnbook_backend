# coding=utf-8
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, ChapterTemplate, Paragraph, \
    BookSeries, IllustrationFile
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, BookSeriesCreateSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer

    @action(detail=False, methods=['post'])
    def complete_create(self, request):
        """
        假定上传的为复合 json结构，一次性上传创建所有相关数据；
        {"name": }
        """
        return Response({"detail": "创建成功"}, status=status.HTTP_201_CREATED)


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


class IllustrationFileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        pic_file = request.data['file']
        IllustrationFile(pic_file=pic_file, user=request.user)
        return Response(status=204)
