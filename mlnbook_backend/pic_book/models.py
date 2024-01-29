# coding=utf-8
import hashlib
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager

# from mlnbook_backend.tts_labs.models import TTSJobInstance
from mlnbook_backend.utils.global_choices import LANGUAGE_CODE_CHOICES, LANGUAGE_LEVEL, PHASE_LEVEL, GRADE_LEVEL, \
    AZURE_VOICE_STYLE
from mlnbook_backend.users.models import Author
from mlnbook_backend.utils.tools import gen_para_ssml

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
    coqui使用说明：
    $tts --model_name "<model_type>/<language>/<dataset>/<model_name>" \
        --vocoder_name "<model_type>/<language>/<dataset>/<model_name>"
    $tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/glow-tts" \
        --vocoder_name "vocoder_models/en/ljspeech/univnet" --out_path output/path/speech.wav

    当 para_ssml 无值时，使用 para_content；
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="speaker-xxxxxxxx">
            <mstts:express-as  style="angry" >
                <prosody rate="0%" pitch="0%">
                {{para_content}}
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>

    para_ssml有值，且以<voice开头，则：
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        {{para_ssml}}
    </speak>

    其他情况：
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="speaker-xxxxxxxx">
            {{para_ssml}}
        </voice>
    </speak>
    """
    title = models.CharField("标题", max_length=500)
    language = models.CharField("语言", max_length=16, default="en_US", help_text="language-ios_code, coqui保存路径")
    tts_model = models.CharField("tts模型", max_length=20, default="azure-api",
                                 help_text="开源TTS算法 coqui-ai, 微软语音服务 azure-api; 人工 manual")
    voice_name = models.CharField("主语音编码", max_length=100, blank=True, null=True)
    style = models.CharField("说话风格", max_length=100, blank=True, null=True, choices=AZURE_VOICE_STYLE)
    pitch = models.SmallIntegerField("音调", default=0, help_text="最大+50%，最小-50%")
    rate = models.SmallIntegerField("语速", default=0, help_text="最大+200%，最小-100%")
    # volume = models.SmallIntegerField("音量", default=100, help_text="最大100，最小0")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_template"

    def __str__(self):
        return "%s|%s" % (self.id, self.title)


class PicBook(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    tags = TaggableManager(blank=True)
    phase = models.CharField("学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("年级", max_length=30, choices=GRADE_LEVEL, default="age2-preschool")
    cover_img = models.ImageField("封面图", max_length=500, blank=True, null=True)
    author = models.ManyToManyField(Author)
    voice_template = models.ManyToManyField(VoiceTemplate, through='PicBookVoiceTemplateRelation', blank=True)
    state = models.SmallIntegerField("绘本状态", default=0, choices=BOOK_STATE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_pic_books"

    def __str__(self):
        return "%s|%s" % (self.id, self.title)


class PicBookVoiceTemplateRelation(models.Model):
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    voice_state = models.SmallIntegerField("绘本语音状态", default=0, choices=VOICE_STATE_CHOICES)
    seq = models.SmallIntegerField("排序", default=1, help_text="排序最小的为默认")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_voice_template_book_relation"
        unique_together = ["pic_book", "voice_template"]
        ordering = ["seq"]

    def __str__(self):
        return "%s|%s|%s" % (self.id, self.pic_book.title, self.voice_template.title)


class BookSeries(models.Model):
    title = models.CharField("标题", max_length=500)
    description = models.CharField("描述信息", max_length=1000, null=True, blank=True)
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    tags = TaggableManager(blank=True)
    pic_books = models.ManyToManyField(PicBook)
    share_state = models.CharField("公开状态", max_length=16, default="public")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_book_series"

    def __str__(self):
        return "%s|%s" % (self.id, self.title)


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
    background_img = models.ImageField("背景图面", upload_to="pic_books/background_img/", null=True, blank=True)
    background_color = models.CharField("背景颜色", max_length=16, default="#FFFFFF")
    text_flex_justify = models.CharField("文本主轴位置", max_length=20, default="flex-end",
                                         choices=FLEX_JUSTIFY_OPTIONS,
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
        return "%s|%s" % (self.id, self.title)


class Chapter(models.Model):
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    title = models.CharField("标题", max_length=200)
    text_template = models.TextField("文案模板", max_length=1000, blank=True)
    seq = models.SmallIntegerField("顺序", default=1, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    set_group = models.BooleanField("设为分组", default=False)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_chapter"
        ordering = ["seq"]

    def __str__(self):
        return "%s|%s" % (self.id, self.title)

    def is_leaf(self):
        if self.parent:
            return True
        else:
            return False

    def chapter_selectable(self):
        if self.set_group:
            # 分组不可点
            return False
        else:
            return True


# class IllustrationFile(models.Model):
#     pic_file = models.ImageField("插图", upload_to="pic_books/illustration/", null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ctime = models.DateTimeField(auto_now_add=True)
#     utime = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "mlnbook_pic_book_illustration_file"
#
#     def __str__(self):
#         return self.pic_file.url


class KnowledgePoint(models.Model):
    knowledge_uniq = models.CharField("知识点唯一标识", max_length=64, help_text="content文本MD5加密")
    knowledge = models.CharField("知识内容", max_length=500, help_text="单词或句子，作为段落的一个主题内容")
    language = models.CharField("语言", max_length=16, default="en_US", choices=LANGUAGE_CODE_CHOICES)
    language_level = models.CharField("默认语言级别", max_length=16, default="A1", choices=LANGUAGE_LEVEL)
    tags = TaggableManager(blank=True)
    phase = models.CharField("默认学段", max_length=20, choices=PHASE_LEVEL, default="preschool")
    grade = models.CharField("默认年级", max_length=30, choices=GRADE_LEVEL, default="1t2-preschool")
    illustration = models.ImageField("默认插图", max_length=500, blank=True, null=True)
    # voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE, null=True)
    # pic_style = models.CharField("图片风格", max_length=20, default="realistic")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_knowledge_point"
        unique_together = ["knowledge_uniq", "language"]

    def save(self, *args, **kwargs):
        self.knowledge_uniq = hashlib.md5(self.knowledge.strip().lower().encode("utf-8")).hexdigest()
        super(KnowledgePoint, self).save(*args, **kwargs)

    def __str__(self):
        return "%s|%s" % (self.id, self.knowledge)

    def illustration_url(self):
        return self.illustration.url


# class BookPage(models.Model):
#     pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
#     seq = models.IntegerField("页码顺序", default=1, db_index=True, help_text="当前为章节内部排序")
#     layout = models.ForeignKey(LayoutTemplate, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ctime = models.DateTimeField(auto_now_add=True)
#     utime = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "mlnbook_pic_book_page"
#         ordering = ["seq"]
#
#     def get_menu_key(self):
#         # 前端节点唯一标识
#         return "leaf_%s" % self.id
#
#     def get_title(self):
#         return "PageID_%s" % self.id
#
#     def get_parent(self):
#         return self.chapter_id
#
#     def __str__(self):
#         return "chapter_%s|page_%s" % (self.chapter.title, self.seq)


class Typeset(models.Model):
    """
    norm： 1x1, 2x2； pic_book，设定settings；
    custom: 按章节定制， pic_book【无settings值】； chapter 设定 settings；
    """
    title = models.CharField("标题", max_length=200)
    c_type = models.CharField("排版类型", max_length=15, default="norm",
                              help_text="norm 标准化的； custom 人工定制的")
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    setting = models.JSONField("设定", blank=True, null=True,
                               help_text="结构为 [[layoutID, layoutID, layoutID], [layoutID, layoutID]]; 每行为一章内容")
    seq = models.IntegerField("页码顺序", default=1, db_index=True, help_text="当前为章节内部排序")
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_typeset"
        ordering = ["seq"]


class ChapterTypeset(models.Model):
    """
    norm： 1x1, 2x2； pic_book，设定settings；
    custom: 按章节定制， pic_book【无settings值】； chapter 设定 settings；
    """
    typeset = models.ForeignKey(Typeset, on_delete=models.CASCADE)
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    setting = models.JSONField("设定", blank=True, null=True,
                               help_text="结构为 [[layoutID, layoutID, layoutID], [layoutID, layoutID]]; 每行为一章内容")
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_custom_chapter_typeset"
        ordering = ["seq"]


class Paragraph(models.Model):
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    para_content = models.TextField("段落内容", help_text="段落内容；一般基于知识点+章节复合生成")
    para_ssml = models.TextField("段落的ssml语音", blank=True,
                                 help_text="判断是否以<voice开头，<speak>下面，否则放在<voice>下面")
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密", blank=True)
    knowledge = models.CharField("知识点", max_length=200, null=True, blank=True)
    knowledge_uniq = models.CharField("知识点MD5", max_length=64, null=True, blank=True,
                                      help_text="对知识点前后去空格，转小写，MD5加密")
    illustration = models.ImageField("插图", max_length=500, blank=True, null=True)
    seq = models.SmallIntegerField("章节内排序", default=1, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph"
        unique_together = ["chapter", "para_content_uniq"]
        ordering = ["seq"]

    def save(self, *args, **kwargs):
        self.para_content_uniq = hashlib.md5(self.para_content.strip().lower().encode("utf-8")).hexdigest()
        if self.knowledge:
            self.knowledge_uniq = hashlib.md5(self.knowledge.strip().lower().encode("utf-8")).hexdigest()
        super(Paragraph, self).save(*args, **kwargs)

    def __str__(self):
        return "%s|%s" % (self.id, self.para_content)


class ParagraphVoiceFile(models.Model):
    # 例行写入；人工上传？
    pic_book = models.ForeignKey(PicBook, on_delete=models.CASCADE)
    voice_template = models.ForeignKey(VoiceTemplate, on_delete=models.CASCADE)
    para_content_uniq = models.CharField("段落内容唯一标识", max_length=64, help_text="content文本MD5加密")
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file", blank=True, null=True)
    duration = models.IntegerField("毫秒", default=1000)
    para_ssml = models.TextField("语音ssml", blank=True)
    job_state = models.SmallIntegerField("任务状态", default=0)
    job_detail = models.TextField("任务执行信息", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_pic_book_paragraph_voice_file"
        unique_together = ["pic_book", "para_content_uniq", "voice_template"]

    def __str__(self):
        if self.voice_file:
            return self.voice_file.url
        else:
            return "%s" % self.id


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


@receiver(post_save, sender=Paragraph)
def create_knowledge(sender, instance, created, **kwargs):
    if created:
        try:
            knowledge_obj = KnowledgePoint.objects.get(knowledge_uniq=instance.knowledge_uniq)
            print("existed knowledge: %s" % knowledge_obj.knowledge)
        except KnowledgePoint.DoesNotExist:
            new_obj = KnowledgePoint(knowledge=instance.knowledge,
                                     knowledge_uniq=instance.knowledge_uniq,
                                     language=instance.pic_book.language,
                                     language_level=instance.pic_book.language_level,
                                     illustration=instance.illustration,
                                     phase=instance.pic_book.phase,
                                     grade=instance.pic_book.grade,
                                     user=instance.user)
            new_obj.save()

#
# @receiver(post_save, sender=Paragraph)
# def sync_paragraph_voice(sender, instance, created, **kwargs):
#     if created:
#         queryset = PicBookVoiceTemplateRelation.objects.filter(pic_book=instance.pic_book)
#         if queryset:
#             # instance 为段落obj
#             for relation_obj in queryset:
#                 voice_cfg = {"voice_name": relation_obj.voice_template.voice_name,
#                              "style": relation_obj.voice_template.style,
#                              "pitch": relation_obj.voice_template.pitch,
#                              "rate": relation_obj.voice_template.rate
#                              }
#                 new_obj = ParagraphVoiceFile(pic_book=relation_obj.pic_book,
#                                              voice_template=relation_obj.voice_template,
#                                              para_content_uniq=instance.para_content_uniq,
#                                              para_ssml=gen_para_ssml(instance.para_content, instance.para_ssml,
#                                                                      voice_cfg),
#                                              user=instance.user
#                                              )
#                 new_obj.save()
