# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.pic_book.models import PicBook, BookSeries, KnowledgePoint, Paragraph, ChapterTemplate


class PicBookSerializer(serializers.ModelSerializer):
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


class ChapterTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChapterTemplate
        fields = ["id", "title", "description", "c_type", "text_template", "grid_layout", "user",
                  "font_color", "font_family", "font_size", "background_img", "background_color",
                  "text_position", "text_opacity", "voice_template", "ctime", "utime"]


class KnowledgePointSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgePoint
        fields = ["id", "knowledge_uniq", "knowledge", "language", "language_level", "phase", "grade", "pic_style",
                  "user", "ctime", "utime"]


class ParagraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paragraph
        fields = ["id", "paragraph_uniq", "pic_book", "chapter", "knowledge_point", "para_content", "illustration",
                  "page_num", "page_para_seq", "user", "utime"]


class PicBookCompleteSerializer(serializers.ModelSerializer):
    pic_book = PicBookSerializer()
    chapter = ChapterTemplateSerializer()
    knowledge_point = KnowledgePointSerializer()

    class Meta:
        model = Paragraph
        fields = ["id", "paragraph_uniq", "pic_book", "chapter", "knowledge_point", "para_content", "illustration",
                  "page_num", "page_para_seq", "user", "utime"]
