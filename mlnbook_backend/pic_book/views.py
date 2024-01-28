# coding=utf-8
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from mlnbook_backend.pic_book.tasks import paragraph_voice_file_task

from mlnbook_backend.pic_book.models import PicBook, KnowledgePoint, Chapter, Paragraph, \
    BookSeries, LayoutTemplate, VoiceTemplate, ParagraphVoiceFile, PicBookVoiceTemplateRelation
from mlnbook_backend.pic_book.serializers import PicBookSerializer, KnowledgePointSerializer, \
    ChapterSerializer, LayoutTemplateSerializer, ParagraphSerializer, BookSeriesListSerializer, \
    BookSeriesCreateSerializer, PicBookEditSerializer, VoiceTemplateSerializer, ParagraphBulkSerializer, \
    ParagraphVoiceFileSerializer, PicBookVoiceTemplateRelationSerializer, PicBookVoiceTemplateRelationCreateSerializer, \
    ChapterMenuSerializer, ChapterParagraphSerializer

from mlnbook_backend.users.models import Author
from mlnbook_backend.users.serializers import AuthorSerializer
from mlnbook_backend.utils.tools import gen_seq_queryset, gen_para_ssml


class VoiceTemplateViewSet(viewsets.ModelViewSet):
    queryset = VoiceTemplate.objects.all()
    serializer_class = VoiceTemplateSerializer


class PicBookVoiceViewSet(viewsets.ModelViewSet):
    queryset = PicBookVoiceTemplateRelation.objects.all()
    serializer_class = PicBookVoiceTemplateRelationSerializer
    filterset_fields = ['pic_book', 'voice_template']

    def get_serializer_class(self):
        if self.action in ["create"]:
            return PicBookVoiceTemplateRelationCreateSerializer
        else:
            return PicBookVoiceTemplateRelationSerializer

    @action(detail=False, methods=["post"])
    def paragraph_voice_file(self, request, pk=None):
        pic_book = request.data["pic_book"]
        voice_template = request.data["voice_template"]
        para_content_uniq = request.data["para_content_uniq"]
        queryset = PicBookVoiceTemplateRelation.objects.filter(pic_book_id=pic_book, voice_template_id=voice_template)
        if not queryset:
            return Response({"detail": "绘本语音模板不存在"}, status=status.HTTP_400_BAD_REQUEST)
        relation_obj = queryset[0]
        voice_cfg = {"voice_name": relation_obj.voice_template.voice_name,
                     "style": relation_obj.voice_template.style,
                     "pitch": relation_obj.voice_template.pitch,
                     "rate": relation_obj.voice_template.rate
                     }
        para_queryset = Paragraph.objects.filter(pic_book_id=pic_book, para_content_uniq=para_content_uniq)
        # ParagraphVoiceFile.objects.filter(pic_book_id=pic_book).delete()
        voice_file_list = [
            ParagraphVoiceFile(pic_book=relation_obj.pic_book,
                               voice_template=relation_obj.voice_template,
                               para_content_uniq=item.para_content_uniq,
                               para_ssml=gen_para_ssml(item.para_content, item.para_ssml,
                                                       voice_cfg),
                               user=item.user
                               ) for item in para_queryset
        ]
        ParagraphVoiceFile.objects.bulk_create(voice_file_list)
        # 调用tts api接口
        paragraph_voice_file_task.delay(pic_book, voice_template)
        return Response({"detail": "success"})

    @action(detail=False, methods=["post"])
    def bulk_gen_voice_files(self, request, pk=None):
        pic_book = request.data["pic_book"]
        voice_template = request.data["voice_template"]
        queryset = PicBookVoiceTemplateRelation.objects.filter(pic_book_id=pic_book, voice_template_id=voice_template)
        if not queryset:
            return Response({"detail": "绘本语音模板不存在"}, status=status.HTTP_400_BAD_REQUEST)
        relation_obj = queryset[0]
        voice_cfg = {"voice_name": relation_obj.voice_template.voice_name,
                     "style": relation_obj.voice_template.style,
                     "pitch": relation_obj.voice_template.pitch,
                     "rate": relation_obj.voice_template.rate
                     }
        para_queryset = Paragraph.objects.filter(pic_book_id=pic_book)
        ParagraphVoiceFile.objects.filter(pic_book_id=pic_book).delete()
        voice_file_list = [
            ParagraphVoiceFile(pic_book=relation_obj.pic_book,
                               voice_template=relation_obj.voice_template,
                               para_content_uniq=item.para_content_uniq,
                               para_ssml=gen_para_ssml(item.para_content, item.para_ssml,
                                                       voice_cfg),
                               user=item.user
                               ) for item in para_queryset
        ]
        ParagraphVoiceFile.objects.bulk_create(voice_file_list)
        # 调用tts api接口
        paragraph_voice_file_task.delay(pic_book, voice_template)
        return Response({"detail": "success"})


class ParagraphVoiceFileViewSet(viewsets.ModelViewSet):
    queryset = ParagraphVoiceFile.objects.all()
    serializer_class = ParagraphVoiceFileSerializer
    filterset_fields = ['pic_book', 'voice_template', 'para_content_uniq']


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PicBookEditSerializer
        else:
            return PicBookSerializer

    @action(detail=True)
    def voice_list(self, request, pk=None):
        pic_book = self.get_object()
        queryset = PicBookVoiceTemplateRelation.objects.filter(pic_book=pic_book)
        resp_data = PicBookVoiceTemplateRelationSerializer(queryset, many=True).data
        para_queryset = Paragraph.objects.filter(pic_book=pic_book)
        para_data = ParagraphSerializer(para_queryset, many=True).data
        voice_queryset = ParagraphVoiceFile.objects.filter(pic_book=pic_book)
        voice_data = ParagraphVoiceFileSerializer(voice_queryset, many=True).data
        return Response({"book_voice_relation": resp_data, "paragraph": para_data, "voice_files": voice_data})

    # @staticmethod
    # def gen_chapter_page_menu(root_chapter_queryset):
    #     chapter_list = []
    #     for chapter_obj in root_chapter_queryset:
    #         # 当前仅支持一层子级目录
    #         chapter_page_data = ChapterPageMenuSerializer(chapter_obj).data
    #         chapter_page_data["children"] = chapter_page_data.pop("bookpage_set")
    #         children_chapter_queryset = chapter_obj.children.all()
    #         # print(chapter_obj.id, chapter_page_data["children"])
    #         if children_chapter_queryset.exists():
    #             children_data = ChapterPageMenuSerializer(children_chapter_queryset, many=True).data
    #             for item in children_data:
    #                 item["children"] = item.pop("bookpage_set")
    #             chapter_page_data["children"] += children_data
    #             # print(chapter_obj.id, children_data)
    #         sorted_data = sorted(chapter_page_data["children"], key=lambda x: x['seq'])
    #         chapter_page_data["children"] = sorted_data
    #         chapter_list.append(chapter_page_data)
    #     return chapter_list
    #
    # @action(detail=True)
    # def chapter_page_menu(self, request, pk=None):
    #     pic_book = self.get_object()
    #     root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
    #     chapter_list = self.gen_chapter_page_menu(root_chapter_queryset)
    #     return Response(chapter_list)

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

    # @action(detail=True)
    # def page_nums(self, request, pk=None):
    #     pic_book = self.get_object()
    #     chapter_queryset = Chapter.objects.filter(pic_book=pic_book)
    #     has_parent_chapter = chapter_queryset.exclude(parent__isnull=True)
    #     page_num_dict = {}
    #     if not has_parent_chapter.exists():
    #         # 没有子章嵌套直接排序
    #         page_id_list = list(BookPage.objects.filter(pic_book=pic_book).values_list("id", flat=True))
    #         for num, val in enumerate(page_id_list, start=1):
    #             page_num_dict[val] = num
    #     else:
    #         # 存在子章嵌套
    #         parent_chapter_queryset = chapter_queryset.filter(parent__isnull=True)
    #         chapter_list = self.gen_chapter_page_menu(parent_chapter_queryset)
    #         page_id_list = []
    #         for page_child_list in chapter_list:
    #             for item in page_child_list:
    #                 if "isLeaf" in item:
    #                     page_id_list.append(item)
    #                 else:
    #                     page_id_list.extend(item["children"])
    #         page_num_dict = {each["id"]: each["seq"] for each in page_id_list}
    #     return Response(page_num_dict)

    @staticmethod
    def update_menu_attr(cur_key, attr_value, attr="sort_seq"):
        # if "leaf" in str(cur_key):
        #     obj_id = int(cur_key.split("_")[1])
        #     obj = BookPage.objects.get(id=obj_id)
        #     if attr == "sort_seq":
        #         setattr(obj, "seq", attr_value)
        #     else:
        #         setattr(obj, "chapter_id", attr_value)
        #     obj.save()
        # else:
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

    @action(detail=True)
    def chapter(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterSerializer(chapter_obj, context={"request": self.request}).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                child_serializer = ChapterSerializer(children_chapter_queryset, many=True, context={"request": self.request})
                parent_data["children"] = child_serializer.data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    # @action(detail=True)
    # def chapter_page(self, request, pk=None):
    #     pic_book = self.get_object()
    #     root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
    #     chapter_list = []
    #     for chapter_obj in root_chapter_queryset:
    #         # 一层子级目录
    #         parent_data = ChapterPageSerializer(chapter_obj, context={"request": self.request}).data
    #         children_chapter_queryset = chapter_obj.children.all()
    #         if children_chapter_queryset.exists():
    #             child_serializer = ChapterPageSerializer(children_chapter_queryset, many=True, context={"request": self.request})
    #             parent_data["children"] = child_serializer.data
    #         chapter_list.append(parent_data)
    #     return Response(chapter_list)

    @action(detail=True)
    def chapter_page_paragraph(self, request, pk=None):
        pic_book = self.get_object()
        root_chapter_queryset = Chapter.objects.filter(pic_book=pic_book, parent__isnull=True)
        chapter_list = []
        for chapter_obj in root_chapter_queryset:
            # 一层子级目录
            parent_data = ChapterParagraphSerializer(chapter_obj, context={"request": self.request}).data
            children_chapter_queryset = chapter_obj.children.all()
            if children_chapter_queryset.exists():
                child_serializer = ChapterParagraphSerializer(children_chapter_queryset, many=True, context={"request": self.request})
                parent_data["children"] = child_serializer.data
            chapter_list.append(parent_data)
        return Response(chapter_list)

    @action(detail=True)
    def preview(self, request, pk=None):
        pic_book = self.get_object()
        # 书籍的语音
        voice_queryset = ParagraphVoiceFile.objects.filter(pic_book=pic_book)
        voice_data = ParagraphVoiceFileSerializer(voice_queryset, many=True).data
        # 页面内容
        book_page_queryset = BookPage.objects.filter(pic_book=pic_book)
        bookpage_data = BookPageSerializer(book_page_queryset, many=True).data

        # 布局模板
        layout_data = LayoutTemplateSerializer(LayoutTemplate.objects.all(), many=True).data
        layout_map = {item['id']: item for item in layout_data}

        # 段落内容
        para_queryset = Paragraph.objects.filter(pic_book=pic_book)
        para_data = ParagraphSerializer(para_queryset, many=True).data
        para_page_map = {}
        for q in para_data:
            para_page_map.setdefault(q['book_page'], [])
            para_page_map[q['book_page']].append(q)
        # 拼接内容
        for item in bookpage_data:
            item['paragraph'] = para_page_map.get(item['id'], {})
            item['layout_cfg'] = layout_map.get(item['layout'], {})
        book_preview = {
            "id": pic_book.id,
            "title": pic_book.title,
            "bookpage_set": bookpage_data,
            "voice_files": voice_data
        }
        return Response(book_preview)


class KnowledgePointViewSet(viewsets.ModelViewSet):
    queryset = KnowledgePoint.objects.all()
    serializer_class = KnowledgePointSerializer


class LayoutTemplateViewSet(viewsets.ModelViewSet):
    queryset = LayoutTemplate.objects.all()
    serializer_class = LayoutTemplateSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    # @action(detail=True)
    # def page(self, request, pk=None):
    #     chapter = self.get_object()
    #     bookpage_queryset = chapter.bookpage_set.all()
    #     serializer = BookPageSerializer(bookpage_queryset, many=True)
    #     return Response(serializer.data)

    @action(detail=True)
    def paragraph(self, request, pk=None):
        chapter = self.get_object()
        queryset = chapter.paragraph_set.all()
        serializer = ParagraphSerializer(queryset, many=True)
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

    # def get_serializer_class(self):
    #     if self.action in ["create", "list", "retrieve"]:
    #         return BookPageParagraphSerializer
    #     else:
    #         return BookPageSerializer

    @action(detail=True)
    def paragraph(self, request, pk=None):
        page = self.get_object()
        paragraph_queryset = page.paragraphs.all()
        serializer = ParagraphSerializer(paragraph_queryset, many=True, context={"request": self.request})
        return Response(serializer.data)

    @action(detail=True)
    def chapter_paragraph(self, request, pk=None):
        page = self.get_object()
        paragraph_queryset = page.paragraphs.all()
        serializer = ParagraphSerializer(paragraph_queryset, many=True, context={"request": self.request})
        # 补充章节信息
        chapter = ChapterSerializer(page.chapter)
        resp_data = {
            "paragraph": serializer.data,
            "chapter": chapter.data
        }
        return Response(resp_data)

    @action(detail=False, methods=['post'])
    def set_seq(self):
        seq_list = self.request.data["seq_list"]
        queryset = gen_seq_queryset(seq_list, BookPage)
        BookPage.objects.bulk_update(queryset, ["seq"])
        return Response({"detail": "更新成功"})


class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
    filterset_fields = ['pic_book', 'chapter', 'book_page']

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
    def set_seq(self, request, *args, **kwargs):
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


# class IllustrationFileUploadView(APIView):
#     parser_classes = [FileUploadParser]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, filename, format=None):
#         pic_file = request.data['file']
#         IllustrationFile(pic_file=pic_file, user=request.user)
#         return Response({"detail": "success"})

# class IllustrationFileUploadView(viewsets.ModelViewSet):
#     # parser_classes = [FileUploadParser]
#     serializer_class = IllustrationFileSerializer
#     queryset = IllustrationFile.objects.all()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
