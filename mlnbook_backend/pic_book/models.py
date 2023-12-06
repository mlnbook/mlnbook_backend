# coding=utf-8
from django.db import models
from taggit.managers import TaggableManager

from mlnbook_backend.utils.global_choices import LANGUAGE_CODE_CHOICES, LANGUAGE_LEVEL, PHASE_LEVEL, GRADE_LEVEL
from mlnbook_backend.users.models import Author

CHAPTER_TYPE_CHOICES = (
    ("public", "完全公开"),
    ("protected", "内部使用"),
    ("private", "私人&平台不可用"),
)


class PicBook(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    tags = TaggableManager()
    phase = models.CharField("学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("年级", max_length=30, choices=GRADE_LEVEL, default="age2-preschool")
    cover_img = models.ImageField("封面图", max_length=500, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_pic_books"

    def __str__(self):
        return self.title


class BookSeries(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    tags = TaggableManager()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pic_books = models.ManyToManyField(PicBook)
    share_state = models.CharField("公开状态", max_length=16, default="public")
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_book_series"

    def __str__(self):
        return self.title


class VoiceTemplate(models.Model):
    title = models.CharField("标题", max_length=500)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    speaker = models.CharField("语音文件", max_length=50, blank=True)
    tts_model = models.CharField("使用tts模型", max_length=20, default="coqui-xld1")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_template"

    def __str__(self):
        return self.title


class ChapterTemplate(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    c_type = models.CharField("章节类型", max_length=16, default="protected", choices=CHAPTER_TYPE_CHOICES,
                              help_text="public完全公开共享；protected内置受保护，仅平台可用；private私人创建，平台和其他人不可用")
    # language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    text_template = models.TextField("文案模板", blank=True)
    # 风格样式； style_template = models.ForeignKey(StyleTemplate, on_delete=models.CASCADE)
    grid_layout = models.CharField("栅格布局", max_length=200, help_text="单页面内图片，1*1, 2*2, 3*3, 2*4布局")
    font_color = models.CharField("颜色", max_length=500)
    font_family = models.CharField("字体", max_length=500)
    font_size = models.CharField("文字大小", max_length=500)
    background_img = models.ImageField("背景图面", max_length=500)
    background_color = models.ImageField("背景颜色", max_length=500)
    text_position = models.CharField("文本位置", default="bottom", help_text="文本框在图片中的位置：上中下左右？")
    text_opacity = models.FloatField("文本透明度", default=1, help_text="opacity为不透度度，1为完全显示，0为完全透明; 0.5为半透明 ")
    # voice
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_chapter_template"

    def __str__(self):
        return self.title


class IllustrationFile(models.Model):
    pic_file = models.ImageField("插图", upload_to="pic_books/illustration/", null=True)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_illustration_file"

    def __str__(self):
        return self.pic_file


class KnowledgePoint(models.Model):
    knowledge_uniq = models.CharField("知识点唯一标识", max_length=64, help_text="content文本MD5加密")
    knowledge = models.CharField("知识内容", max_length=500, help_text="单词或句子，作为段落的一个主题内容")
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    tags = TaggableManager()
    phase = models.CharField("学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("年级", max_length=30, choices=GRADE_LEVEL, default="1t2-preschool")
    illustration = models.ForeignKey(IllustrationFile, null=True, on_delete=models.CASCADE)
    # voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE, null=True)
    pic_style = models.CharField("图片风格", default="realistic")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_knowledge_point"
        unique_together = ["knowledge_uniq", "pic_style", "language"]

    def __str__(self):
        return self.knowledge

    def illustration_url(self):
        return self.illustration.pic_file.url


class Paragraph(models.Model):
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    chapter = models.ForeignKey(ChapterTemplate, on_delete=models.CASCADE)
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE, null=True)
    para_content = models.TextField("段落内容", help_text="段落内容；一般基于知识点+章节复合生成")
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    illustration = models.ForeignKey(IllustrationFile, null=True, on_delete=models.CASCADE)
    page_num = models.IntegerField("页码", default=1)
    page_para_seq = models.IntegerField("页内段落排序", default=1)
    # 单页模式，过滤pic_book，按照 page_num + page_para_seq 排序，一个个返回。
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph"
        unique_together = ["pic_book", "chapter", "para_content_uniq"]

    def __str__(self):
        return self.para_content


class ParagraphVoiceFile(models.Model):
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file")
    duration = models.IntegerField("毫秒", default=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph_voice_file"
        unique_together = ["para_content_uniq", "voice_template"]

    def __str__(self):
        return self.voice_file.url


class KnowledgeVoiceFile(models.Model):
    knowledge_uniq = models.CharField("知识点唯一标识", max_length=64, help_text="content文本MD5加密")
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file")
    duration = models.IntegerField("毫秒", default=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph_voice_file"
        unique_together = ["para_content_uniq", "voice_template"]

    def __str__(self):
        return self.voice_file.url
