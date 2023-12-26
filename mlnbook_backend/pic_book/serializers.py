# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.pic_book.models import PicBook, Chapter, BookPage, Paragraph, LayoutTemplate, \
    BookSeries, KnowledgePoint, VoiceTemplate
from mlnbook_backend.users.serializers import AuthorSerializer
from mlnbook_backend.utils.base_serializer import AuthModelSerializer


class PicBookSerializer(AuthModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = PicBook
        fields = ['id', 'title', 'description', 'language', 'language_level', 'phase', 'grade', 'cover_img', 'author',
                  'voice_template', 'voice_state', 'state', 'utime']


class VoiceTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceTemplate
        fields = ['id', 'title', 'language', 'tts_model', 'model_name']


class PicBookEditSerializer(AuthModelSerializer):

    class Meta:
        model = PicBook
        fields = ['id', 'title', 'description', 'language', 'language_level', 'phase', 'grade', 'cover_img', 'author',
                  'voice_template', 'voice_state', 'state']


class BookSeriesListSerializer(AuthModelSerializer):
    pic_books = PicBookSerializer(many=True, read_only=True)

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']


class BookSeriesCreateSerializer(AuthModelSerializer):
    pic_books = serializers.PrimaryKeyRelatedField(many=True, queryset=PicBook.objects.all())

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']


class LayoutTemplateSerializer(AuthModelSerializer):

    class Meta:
        model = LayoutTemplate
        fields = ["id", "title", "description", "c_type", "grid_row_col", "grid_gutter",
                  "font_color", "font_family", "font_size", "background_img", "background_color",
                  "text_flex_justify", "text_flex_align", "text_opacity", "ctime", "utime"]


class ChapterSerializer(AuthModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "title", "pic_book", "text_template", "seq", "utime"]


class BookPageSerializer(AuthModelSerializer):
    class Meta:
        model = BookPage
        fields = ["id", "page_num", "pic_book", "chapter", "layout", "utime"]


class KnowledgePointSerializer(AuthModelSerializer):

    class Meta:
        model = KnowledgePoint
        fields = ["id", "knowledge_uniq", "knowledge", "language", "language_level", "phase", "grade", "pic_style",
                  "ctime", "utime"]


class ParagraphSerializer(AuthModelSerializer):
    illustration_url = serializers.CharField(source='get_illustration_url', read_only=True)

    class Meta:
        model = Paragraph
        fields = ["id", "para_content_uniq", "book_page", "knowledge_point", "para_content", "illustration",
                  "illustration_url", "seq", "utime"]


class ParagraphBulkCreateUpdateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        para_data = [Paragraph(**item) for item in validated_data]
        return Paragraph.objects.bulk_create(para_data)


class ParagraphBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["id", "para_content_uniq", "book_page", "knowledge_point", "para_content", "illustration",
                  "seq", "utime"]
        read_only_fields = ['id', ]
        list_serializer_class = ParagraphBulkCreateUpdateSerializer


class BookPageParagraphSerializer(AuthModelSerializer):
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = BookPage
        fields = ["id", "pic_book", "page_num", "chapter", "layout", "utime", "paragraphs"]

    def create(self, validated_data):
        paragraphs_data = validated_data.pop('paragraphs')
        book_page = BookPage.objects.create(**validated_data)
        for paragraph_data in paragraphs_data:
            Paragraph.objects.create(book_page=book_page, **paragraph_data)
        return book_page


class ChapterPageSerializer(AuthModelSerializer):
    bookpage_set = BookPageSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "text_template", "seq", "utime", "bookpage_set"]


class ChapterParagraphSerializer(AuthModelSerializer):
    bookpage_set = BookPageParagraphSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "text_template", "seq", "utime", "bookpage_set"]
