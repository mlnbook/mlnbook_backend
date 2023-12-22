# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.pic_book.models import PicBook, Chapter, BookPage, Paragraph, LayoutTemplate, \
    BookSeries, KnowledgePoint
from mlnbook_backend.users.serializers import AuthorSerializer


class PicBookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = PicBook
        fields = ['id', 'title', 'description', 'language', 'language_level', 'phase', 'grade', 'author', 'utime']


class BookSeriesListSerializer(serializers.ModelSerializer):
    pic_books = PicBookSerializer(many=True, read_only=True)

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']


class BookSeriesCreateSerializer(serializers.ModelSerializer):
    pic_books = serializers.PrimaryKeyRelatedField(many=True, queryset=PicBook.objects.all())

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']


class LayoutTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayoutTemplate
        fields = ["id", "title", "description", "c_type", "grid_row_col", "grid_gutter", "user",
                  "font_color", "font_family", "font_size", "background_img", "background_color",
                  "text_flex_justify", "text_flex_align", "text_opacity", "ctime", "utime"]


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["id", "title", "text_template", "seq", "user", "utime"]


class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = ["id", "page_num", "pic_book", "chapter", "layout", "user", "utime"]


class KnowledgePointSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgePoint
        fields = ["id", "knowledge_uniq", "knowledge", "language", "language_level", "phase", "grade", "pic_style",
                  "user", "ctime", "utime"]


class ParagraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paragraph
        fields = ["id", "para_content_uniq", "book_page", "knowledge_point", "para_content", "illustration",
                  "seq", "user", "utime"]


class BookPageParagraphSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True)

    class Meta:
        model = BookPage
        fields = ["id", "page_num", "chapter", "layout", "user", "utime", "paragraphs"]

    def create(self, validated_data):
        paragraphs_data = validated_data.pop('paragraphs')
        book_page = BookPage.objects.create(**validated_data)
        for paragraph_data in paragraphs_data:
            Paragraph.objects.create(book_page=book_page, **paragraph_data)
        return book_page


class ChapterPageSerializer(serializers.ModelSerializer):
    bookpage_set = BookPageSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "text_template", "seq", "user", "utime", "bookpage_set"]


class ChapterParagraphSerializer(serializers.ModelSerializer):
    bookpage_set = BookPageParagraphSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "text_template", "seq", "user", "utime", "bookpage_set"]
