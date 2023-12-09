# coding=utf-8
from django.contrib import admin

from mlnbook_backend.pic_book.models import PicBook, BookSeries, ChapterTemplate, KnowledgePoint, Paragraph


@admin.register(PicBook)
class PicBookAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "language", "language_level", "phase", "grade", "author", "ctime"]
    search_fields = ["title"]
    list_filter = ["language", "language_level", "phase"]


@admin.register(BookSeries)
class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "language", "author", "share_state", "ctime"]
    search_fields = ["title"]
    list_filter = ["share_state", "language"]


@admin.register(ChapterTemplate)
class ChapterTemplateAdmin(admin.ModelAdmin):
    list_display = ["c_type", "title", "description", "author", "text_template", "ctime"]
    search_fields = ["title"]
    list_filter = ["c_type", ]


@admin.register(KnowledgePoint)
class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ["knowledge_uniq", "knowledge", "language", "language_level", "phase", "grade", "author", "ctime"]
    search_fields = ["knowledge"]
    list_filter = ["language", "language_level", "phase"]


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ["para_content_uniq", "pic_book", "chapter", "knowledge_point", "para_content",
                    "page_num", "page_para_seq", "author", "ctime"]
    search_fields = ["para_content"]
