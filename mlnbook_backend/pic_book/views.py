# coding=utf-8
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, Chapter, Paragraph, \
    BookSeries, IllustrationFile, LayoutTemplate, BookPage, VoiceTemplate
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterSerializer, LayoutTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, \
    BookSeriesCreateSerializer, BookPageSerializer, BookPageParagraphSerializer, ChapterParagraphSerializer, \
    ChapterPageSerializer, PicBookEditSerializer, VoiceTemplateSerializer, ParagraphBulkSerializer, \
    ChapterMenuSerializer, ChapterPageMenuSerializer

from mlnbook_backend.users.models import Author
from mlnbook_backend.users.serializers import AuthorSerializer
from mlnbook_backend.utils.tools import gen_seq_queryset


class VoiceTemplateViewSet(viewsets.ModelViewSet):
    queryset = VoiceTemplate.objects.all()
    serializer_class = VoiceTemplateSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PicBookEditSerializer
        else:
            return PicBookSerializer

    @action(detail=True)
    def chapter(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterSerializer(chapter_obj).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                child_serializer = ChapterSerializer(children_chapter_queryset, many=True)
                parent_data["children"] = child_serializer.data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @action(detail=True)
    def chapter_page(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterPageSerializer(chapter_obj).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                child_serializer = ChapterPageSerializer(children_chapter_queryset, many=True)
                parent_data["children"] = child_serializer.data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @action(detail=True)
    def chapter_page_paragraph(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterParagraphSerializer(chapter_obj).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                child_serializer = ChapterParagraphSerializer(children_chapter_queryset, many=True)
                parent_data["children"] = child_serializer.data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @action(detail=True)
    def chapter_page_menu(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterPageMenuSerializer(chapter_obj).data
            parent_data["children"] = parent_data.pop("bookpage_set")
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                children_data = ChapterPageMenuSerializer(children_chapter_queryset, many=True).data
                for item in children_data:
                    item["children"] = item.pop("bookpage_set")
                parent_data["children"] = children_data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @action(detail=True)
    def chapter_menu(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterMenuSerializer(chapter_obj).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                children_data = ChapterMenuSerializer(children_chapter_queryset, many=True).data
                parent_data["children"] = children_data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @staticmethod
    def update_menu_attr(cur_key, attr_value, attr="sort_seq"):
        if "leaf" in str(cur_key):
            obj_id = int(cur_key.split("_")[1])
            obj = BookPage.objects.get(id=obj_id)
            if attr == "sort_seq":
                setattr(obj, "seq", attr_value)
            else:
                setattr(obj, "chapter_id", attr_value)
            obj.save()
        else:
            obj = Chapter.objects.get(id=int(cur_key))
            if attr == "sort_seq":
                setattr(obj, "seq", attr_value)
            else:
                setattr(obj, "parent_id", attr_value)
            obj.save()

    @action(detail=False, methods=['post'])
    def sort_menu(self, request, pk=None):
        # 上传 node 的当前父节点； node需要知道是否是 isLeaf 叶子节点；更新父节点
        sort_key = request.data["sort_key"]
        target_parent = request.data["target_parent"]
        self.update_menu_attr(sort_key, target_parent, "parent")
        # 上传当前父节点的 子节点，包括子目录和叶子节点；对同一个parent的节点更新排序
        target_children = request.data["target_children"]
        for ind in range(len(target_children)):
            cur_key = target_children[ind]
            self.update_menu_attr(cur_key, ind)
        return Response({"detail": "success"})


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

    @action(detail=False, methods=['post'])
    def set_seq(self):
        """传入顺序id list;
        [21, 12, 14] 当前；
        备选：[{"id":21, "seq": 1},{"id": 12, "seq":2}]
        """
        seq_list = self.request.data["seq_list"]
        queryset = gen_seq_queryset(seq_list, Chapter)
        Chapter.objects.bulk_update(queryset, ["seq"])
        return Response({"detail": "更新成功"})


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

    @action(detail=False, methods=['post'])
    def set_seq(self):
        seq_list = self.request.data["seq_list"]
        queryset = gen_seq_queryset(seq_list, BookPage)
        BookPage.objects.bulk_update(queryset, ["seq"])
        return Response({"detail": "更新成功"})


class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pic_book', 'chapter']

    @action(detail=False, methods=["post"])
    def batch_create(self, request, *args, **kwargs):
        serializer = ParagraphBulkSerializer(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_seq(self):
        seq_list = self.request.data["seq_list"]
        queryset = gen_seq_queryset(seq_list, Paragraph)
        Paragraph.objects.bulk_update(queryset, ["seq"])
        return Response({"detail": "更新成功"})


class BookSeriesViewSet(viewsets.ModelViewSet):
    queryset = BookSeries.objects.all()
    serializer_class = BookSeriesListSerializer

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


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
