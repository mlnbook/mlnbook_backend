# coding=utf-8
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

from mlnbook_backend.utils.global_choices import LANGUAGE_CODE_CHOICES, LANGUAGE_LEVEL, PHASE_LEVEL, GRADE_LEVEL
from mlnbook_backend.users.models import Author

CHAPTER_TYPE_CHOICES = (
    ("public", "完全公开"),
    ("protected", "内部使用"),
    ("private", "私人&平台不可用"),
)

VOICE_STATE_CHOICES = (
    (1, "done"),
    (0, "prepare"),
    (2, "process"),
    (-1, "error"),
)

BOOK_STATE_CHOICES = (
    (1, "online"),
    (-1, "offline"),
    (0, "prepare"),
)


FLEX_JUSTIFY_OPTIONS = (
    ('flex-start', 'flex-start'),
    ('center', 'center'),
    ('flex-end', 'flex-end'),
    ('space-between', 'space-between'),
    ('space-around', 'space-around'),
    ('space-evenly', 'space-evenly'),
)

FLEX_ALIGN_OPTIONS = (
    ('flex-start', 'flex-start'),
    ('center', 'center'),
    ('flex-end', 'flex-end'),
)


class VoiceTemplate(models.Model):
    """
    使用说明：
    $tts --model_name "<model_type>/<language>/<dataset>/<model_name>" \
        --vocoder_name "<model_type>/<language>/<dataset>/<model_name>"
    $tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/glow-tts" \
        --vocoder_name "vocoder_models/en/ljspeech/univnet" --out_path output/path/speech.wav
    """
    title = models.CharField("标题", max_length=500)
    language = models.CharField("语言", max_length=16, default="en_US", help_text="language-ios_code, coqui保存路径")
    tts_model = models.CharField("tts模型", max_length=20, default="coqui-ai",
                                 help_text="开源TTS算法, coqui-ai, SpeechT5-microsoft")
    model_name = models.CharField("模型名称", max_length=20, default="xtts_v1")
    dataset = models.CharField("tts模型数据集", max_length=20, default="ljspeech")
    vocoder = models.CharField("使用tts模型", max_length=20, default="hifigan_v2")
    speaker = models.CharField("语音编码", max_length=50, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_template"

    def __str__(self):
        return self.title


class PicBook(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    tags = TaggableManager()
    phase = models.CharField("学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("年级", max_length=30, choices=GRADE_LEVEL, default="age2-preschool")
    cover_img = models.ImageField("封面图", max_length=500, blank=True, null=True)
    author = models.ManyToManyField(Author)
    # voice
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_state = models.SmallIntegerField("绘本语音状态", default=0, choices=VOICE_STATE_CHOICES)
    state = models.SmallIntegerField("绘本状态", default=0, choices=BOOK_STATE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
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
    pic_books = models.ManyToManyField(PicBook)
    share_state = models.CharField("公开状态", max_length=16, default="public")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_book_series"

    def __str__(self):
        return self.title


class LayoutTemplate(models.Model):
    """
    ant design grid栅格；
    1. 通过 row 在水平方向建立一组 column（简写 col）。
    2. 你的内容应当放置于 col 内，并且，只有 col 可以作为 row 的直接元素。
    3. 栅格系统中的列是指 1 到 24 的值来表示其跨越的范围。例如，三个等宽的列可以使用 <Col span={8} /> 来创建。
    4. 如果一个 row 中的 col 总和超过 24，那么多余的 col 会作为一个整体另起一行排列。
    5. 使用 Row 的 gutter 属性，我们推荐使用 (16+8n)px 作为栅格间隔(n 是自然数)。如果要支持响应式，可以写成 { xs: 8, sm: 16, md: 24, lg: 32 }

    <Row gutter={[16, 24]}>
      <Col span={12}>col-12</Col>
      <Col span={12}>col-12</Col>
    </Row>
    <Row>
      <Col span={12}>col-12</Col>
      <Col span={12}>col-12</Col>
    </Row>
    <Row>
      <Col span={6}>col-6</Col>
      <Col span={6}>col-6</Col>
      <Col span={6}>col-6</Col>
      <Col span={6}>col-6</Col>
    </Row>
    """
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    c_type = models.CharField("类型", max_length=16, default="protected", choices=CHAPTER_TYPE_CHOICES,
                              help_text="public完全公开共享；protected内置受保护，仅平台可用；private私人创建，平台和其他人不可用")
    # 风格样式； style_template = models.ForeignKey(StyleTemplate, on_delete=models.CASCADE)
    grid_row_col = models.CharField("栅格布局", max_length=200, default="[[24]]",
                                    help_text="单个[[24]]; 2x2=4个[[12,12],[12,12]];复杂[[12,12], [12,12], [6,6,6,6]]")
    grid_gutter = models.CharField("栅格间距", max_length=20, default="[16, 24]",
                                   help_text="使用 (16+8n)px 作为栅格间隔(n 是自然数); [Horizontal水平, Vertical垂直]")
    font_color = models.CharField("颜色", max_length=16, default="#0000E0")
    font_family = models.CharField("字体", max_length=50, default="Arial")
    font_size = models.SmallIntegerField("文字大小", default="14", help_text="14px")
    background_img = models.ImageField("背景图面", max_length=500, null=True, blank=True)
    background_color = models.ImageField("背景颜色", max_length=500, default="#FFFFFF")
    text_flex_justify = models.CharField("文本主轴位置", max_length=20, default="flex-end", choices=FLEX_JUSTIFY_OPTIONS,
                                         help_text="Flex弹性布局, 设置元素在主轴方向上的对齐方式")
    text_flex_align = models.CharField("文本交叉轴位置", max_length=20, default="flex-end", choices=FLEX_ALIGN_OPTIONS,
                                       help_text="Flex弹性布局, 设置元素在交叉轴方向上的对齐方式")
    text_opacity = models.FloatField("文本透明度", default=1,
                                     help_text="opacity为不透度度，1为完全显示，0为完全透明; 0.5为半透明 ")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_layout_template"

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField("标题", max_length=200)
    text_template = models.TextField("文案模板", max_length=1000, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_chapter"

    def __str__(self):
        return self.title


class IllustrationFile(models.Model):
    pic_file = models.ImageField("插图", upload_to="pic_books/illustration/", null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
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
    pic_style = models.CharField("图片风格", max_length=20, default="realistic")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
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
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    page = models.IntegerField("页码", default=1)
    layout = models.ForeignKey(LayoutTemplate, on_delete=models.CASCADE, null=True)
    para_content = models.TextField("段落内容", help_text="段落内容；一般基于知识点+章节复合生成")
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE, null=True)
    illustration = models.ForeignKey(IllustrationFile, null=True, on_delete=models.CASCADE)
    para_seq = models.IntegerField("页内段落排序", default=1)
    # 单页模式，过滤pic_book，按照 page_num + page_para_seq 排序，一个个返回。
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph"
        unique_together = ["pic_book", "chapter", "page_num", "para_content_uniq"]

    def __str__(self):
        return self.para_content


class ParagraphVoiceFile(models.Model):
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file")
    duration = models.IntegerField("毫秒", default=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_knowledge_voice_file"
        unique_together = ["knowledge_uniq", "voice_template"]

    def __str__(self):
        return self.voice_file.url
