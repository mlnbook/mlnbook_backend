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

LANGUAGE_LEVEL = (
    ("A1", "入门级，可以做简单的互动与交流"),
    ("A2", "基础级，能理解并使用熟悉的日常表达法，基本词汇以求满足具体的需求"),
    ("B1", "进阶级，能理解大部分日常生活中常用句子和表达法"),
    ("B2", "高阶级，能在与以目标语言为母语的对象做互动时保持一定流畅度"),
    ("C1", "流利运用级，在社交上、学术上及专业的场合中，皆能灵活的有效地运用语言资源"),
    ("C2", "精通级，能流利、准确、并即兴的表达自己的意见，并且在较为复杂的情况下亦能有效地表达或区别出言外之意"),
)

PHASE_LEVEL = (
    ("preschool", "学前班"),  # 体验式教育，游戏和保育为主
    ("Kindergarten", "幼儿园"),  # 课本教育，小学知识预输入；一般持续1年。
    ("elementary_school", "小学"),
    ("middle_school", "中学"),
    ("high_school", "高中"),
    ("university", "大学"),
)

GRADE_LEVEL = (
    ("preschool", "学前班"),  # 体验式教育，游戏和保育为主
    ("Kindergarten", "幼儿园"),  # 课本教育，小学知识预输入；一般持续1年。
    ("Grade1", "小学一年级"),
    ("Grade2", "小学二年级"),
    ("Grade3", "小学三年级"),
    ("Grade4", "小学四年级"),
    ("Grade5", "小学五年级"),
    ("Grade6", "小学六年级"),  # 部分地区无六年级
    ("Grade7", "初中一年级"),
    ("Grade8", "初中二年级"),
    ("Grade9", "初中三年级"),
    ("Grade10", "高中一年级"),
    ("Grade11", "高中二年级"),
    ("Grade12", "高中三年级"),
)

PRESCHOOL_YEARS = (
    ("3mm-12mm", "3-12months"),
    ("12mm-18mm", "12-18months"),
    ("18mm-2yy", "18months-2years"),
    ("2yy-3yy", "2-3years"),
    ("3yy-5yy", "3-5years"),
)

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
    phase = models.CharField("学段", max_length=16, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("学段", max_length=16, choices=GRADE_LEVEL, default="preschool")
    preschool_year = models.CharField("学前学龄", max_length=16, blank=True, help_text="学前课程细分，非学前为空值")
    cover_img = models.ImageField("封面图", max_length=500)
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_pic_books"

    def __str__(self):
        return self.title


class BookSeries(models.Model):
    title = models.CharField("标题", max_length=500)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    author = models.CharField("作者ID", max_length=36)
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


class ChapterTemplate(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    c_type = models.CharField("章节类型", max_length=16, default="protected", choices=CHAPTER_TYPE_CHOICES,
                              help_text="public完全公开共享；protected内置受保护，仅平台可用；private私人创建，平台和其他人不可用")
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
        db_table = "mlnbook_pic_book_chapter_template"

    def __str__(self):
        return self.title


class KnowledgePoint(models.Model):
    knowledge_uniq = models.CharField("知识点唯一标识", max_length=64, help_text="content文本MD5加密")
    knowledge = models.CharField("知识内容", max_length=500, help_text="单词或句子，作为段落的一个主题内容")
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    phase = models.CharField("学段", max_length=16, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("学段", max_length=16, choices=GRADE_LEVEL, default="preschool")
    preschool_year = models.CharField("学前学龄", max_length=16, blank=True, help_text="学前课程细分，非学前为空值")
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
    chapter = models.ForeignKey(ChapterTemplate, on_delete=models.CASCADE)
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE, null=True)
    para_content = models.TextField("段落内容", help_text="段落内容；一般基于知识点+章节复合生成")
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    seq_sort = models.IntegerField("排序", default=1, help_text="章节内容排序")
    author = models.CharField("作者ID", max_length=36)
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph"
        unique_together = ["pic_book", "chapter", "content_uniq"]

    def __str__(self):
        return self.content


class VoiceFile(models.Model):
    knowledge_uniq = models.CharField("知识点唯一标识", max_length=64, help_text="content文本MD5加密")
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file")
    ctime = models.DateTimeField(auto_created=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_file"
        unique_together = ["knowledge_uniq", "content_uniq", "voice_template"]

    def __str__(self):
        return self.voice_file.url
