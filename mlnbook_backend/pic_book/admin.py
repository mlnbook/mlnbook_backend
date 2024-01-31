# coding=utf-8
from django.contrib import admin

from mlnbook_backend.pic_book.models import BookSeries, PicBook, Chapter, LayoutTemplate, \
    KnowledgePoint, Paragraph, KnowledgeVoiceFile, ParagraphVoiceFile, VoiceTemplate, \
    PicBookVoiceTemplateRelation, Typeset, ChapterTypeset


@admin.register(PicBook)
class PicBookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "language", "language_level", "phase", "grade", "user", "ctime"]
    search_fields = ["title"]
    list_filter = ["language", "language_level", "phase"]


@admin.register(BookSeries)
class BookSeriesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "language", "user", "share_state", "ctime"]
    search_fields = ["title"]
    list_filter = ["share_state", "language"]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["id", "pic_book", "title", "text_template", "user", "ctime"]
    search_fields = ["title"]


@admin.register(LayoutTemplate)
class LayoutTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "grid_row_col", "grid_gutter", "user", "c_type", "ctime"]
    search_fields = ["title"]
    list_filter = ["c_type", ]


@admin.register(KnowledgePoint)
class KnowledgePointAdmin(admin.ModelAdmin):
    list_display = ["id", "knowledge_uniq", "knowledge", "language", "language_level", "phase", "grade", "user", "ctime"]
    search_fields = ["knowledge"]
    list_filter = ["language", "language_level", "phase"]


@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ["id", "para_content_uniq", "knowledge", "para_content", "pic_book", "chapter", "illustration",
                    "seq", "user", "ctime"]
    search_fields = ["para_content"]
    list_filter = ["pic_book"]


@admin.register(ParagraphVoiceFile)
class ParagraphVoiceFileAdmin(admin.ModelAdmin):
    list_display = ["id", "para_content_uniq", "voice_template", "voice_file", "duration",
                    "user", "ctime", "utime"]
    search_fields = ["para_content_uniq"]


@admin.register(KnowledgeVoiceFile)
class KnowledgeVoiceFileAdmin(admin.ModelAdmin):
    list_display = ["id", "knowledge_uniq", "voice_template", "voice_file", "duration",
                    "user", "ctime", "utime"]
    search_fields = ["knowledge_uniq"]


# @admin.register(IllustrationFile)
# class IllustrationFileAdmin(admin.ModelAdmin):
#     list_display = ["id", "pic_file", "ctime", "utime"]
#     search_fields = ["id", ]


@admin.register(VoiceTemplate)
class VoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "language", "voice_name", "tts_model",
                    "user", "ctime", "utime"]
    search_fields = ["title"]


@admin.register(PicBookVoiceTemplateRelation)
class PicBookVoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "pic_book", "voice_template", "seq", "voice_state",
                    "ctime", "utime"]


@admin.register(Typeset)
class TypesetAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "c_type", "pic_book", "seq", "is_default"]


@admin.register(ChapterTypeset)
class ChapterTypesetAdmin(admin.ModelAdmin):
    list_display = ["typeset", "chapter", "pic_book", "ctime"]
