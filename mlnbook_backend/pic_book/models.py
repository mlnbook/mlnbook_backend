# coding=utf-8
from django.db import models

# 语言使用排名 https://www.ethnologue.com/
LANGUAGE_CODE_CHOICES = (
    ("en_US", "英语"),
    ("zh_CN", "简体中文"),
    ("fr_FR", "法语"),
    ("es_ES", "西班牙语"),
    ("ar_AE", "阿拉伯语"),
    ("ru_RU", "俄语"),
    # 以上为联合国6种官方语言
    ("pt_BR", "葡萄牙语"),
    ("ja_JP", "日语"),
    ("de_DE", "德语"),
    ("ko_KR", "韩语"),
    ("in_ID", "印尼语"),
    ("ms_MY", "马来语"),
    ("th_TH", "泰语"),
    ("hi_IN", "北印度语"),
    # 印度有多种语言，暂忽略 ("mr_IN", "印度马拉地语"),
    ("tr_TR", "土耳其语"),
    ("it_IT", "意大利语"),
    ("cs_CZ", "捷克语"),
    ("da_DK", "丹麦语"),
    ("nl_NL", "荷兰语"),
    ("no_NO", "挪威语"),
    ("pl_PL", "波兰语"),
    ("ro_RO", "罗马尼亚语"),
    ("sv_SE", "瑞典语"),
    ("tl_PH", "他加禄语-菲律宾"),
)


class BookSeries(models.Model):
    title = models.CharField("标题", max_length=500)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    author = models.CharField("作者ID", max_length=36)
    share_state = models.CharField("公开状态", max_length=16, default="public")
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_pic_book_series"

    def __str__(self):
        return self.title


class PicBook(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    cover_img = models.ImageField("封面图", max_length=500)
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_pic_books"

    def __str__(self):
        return self.title


class VoiceTemplate(models.Model):
    title = models.CharField("标题", max_length=500)
    language = models.CharField()
    speaker = models.CharField()
    tts_model = models.CharField()
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_template"

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    c_type = models.CharField("章节类型", max_length=16, default="private",
                              help_text="分为public和private，公共是模版多本书共享；私有的每本书独享。")
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    text_template = models.TextField("文案模板", blank=True)
    # style_template = models.ForeignKey(StyleTemplate, on_delete=models.CASCADE)
    grid_layout = models.CharField("栅格布局", max_length=200, help_text="单页面内图片，1*1, 2*2, 3*3布局")
    font_color = models.CharField("颜色", max_length=500)
    font_family = models.CharField("颜色", max_length=500)
    font_size = models.CharField("颜色", max_length=500)
    background_img = models.ImageField("背景图面", max_length=500)
    background_color = models.ImageField("背景图面", max_length=500)
    text_position = models.CharField("文本位置", default="bottom", help_text="文本框在图片中的位置：上中下左右？")
    text_opacity = models.FloatField("文本透明度", default=1, help_text="opacity为不透度度，1为完全显示，0为完全透明; 0.5为半透明 ")
    # voice
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_chapter"

    def __str__(self):
        return self.title


class KnowledgePoint(models.Model):
    knowledge_uniq = models.CharField("内容唯一标识", max_length=100, help_text="content文本MD5加密")
    knowledge = models.CharField("内容", max_length=500, help_text="单词或句子，作为段落的一个主题内容")
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    pic_file = models.ImageField("图片", upload_to="/images/keywords", null=True)
    pic_style = models.CharField("图片风格", default="realistic")
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_knowledge_point"
        unique_together = ["content_uniq", "pic_style", "language"]

    def __str__(self):
        return self.knowledge


class Paragraph(models.Model):
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE)
    content = models.TextField("段落内容", help_text="段落内容；一般基于知识点+章节复合生成")
    content_uniq = models.CharField("内容唯一标识", max_length=100, help_text="content文本MD5加密")
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph"
        unique_together = ["content_uniq", "pic_style", "language"]

    def __str__(self):
        return self.content


class VoiceFile(models.Model):
    knowledge_uniq = models.CharField()
    content_uniq = models.CharField()
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file")
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_file"
        unique_together = ["knowledge_uniq", "content_uniq", "voice_template"]

    def __str__(self):
        return self.voice_file.url
