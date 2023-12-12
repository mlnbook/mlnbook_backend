# Generated by Django 4.2.7 on 2023-12-12 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0002_author_profile"),
        ("taggit", "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="IllustrationFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("pic_file", models.ImageField(null=True, upload_to="pic_books/illustration/", verbose_name="插图")),
                ("utime", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_illustration_file",
            },
        ),
        migrations.CreateModel(
            name="KnowledgePoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                (
                    "knowledge_uniq",
                    models.CharField(help_text="content文本MD5加密", max_length=64, verbose_name="知识点唯一标识"),
                ),
                ("knowledge", models.CharField(help_text="单词或句子，作为段落的一个主题内容", max_length=500, verbose_name="知识内容")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en_US", "英语"),
                            ("zh_CN", "简体中文"),
                            ("fr_FR", "法语"),
                            ("es_ES", "西班牙语"),
                            ("ar_AE", "阿拉伯语"),
                            ("ru_RU", "俄语"),
                            ("pt_BR", "葡萄牙语"),
                            ("ja_JP", "日语"),
                            ("de_DE", "德语"),
                            ("ko_KR", "韩语"),
                            ("in_ID", "印尼语"),
                            ("ms_MY", "马来语"),
                            ("th_TH", "泰语"),
                            ("hi_IN", "北印度语"),
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
                        ],
                        default="en_US",
                        max_length=16,
                        verbose_name="语言",
                    ),
                ),
                (
                    "language_level",
                    models.CharField(
                        choices=[
                            ("A1", "入门级，可以做简单的互动与交流"),
                            ("A2", "基础级，能理解并使用熟悉的日常表达法，基本词汇以求满足具体的需求"),
                            ("B1", "进阶级，能理解大部分日常生活中常用句子和表达法"),
                            ("B2", "高阶级，能在与以目标语言为母语的对象做互动时保持一定流畅度"),
                            ("C1", "流利运用级，在社交上、学术上及专业的场合中，皆能灵活的有效地运用语言资源"),
                            ("C2", "精通级，能流利、准确、并即兴的表达自己的意见，并且在较为复杂的情况下亦能有效地表达或区别出言外之意"),
                        ],
                        default="A1",
                        max_length=16,
                        verbose_name="语言级别",
                    ),
                ),
                (
                    "phase",
                    models.CharField(
                        choices=[
                            ("preschool", "学前班"),
                            ("kindergarten", "幼儿园"),
                            ("primary", "小学"),
                            ("middle", "初中"),
                            ("high", "高中"),
                            ("university", "大学"),
                        ],
                        default="preschool",
                        max_length=20,
                        verbose_name="学段",
                    ),
                ),
                (
                    "grade",
                    models.CharField(
                        choices=[
                            ("age1-preschool", "学前1岁"),
                            ("age2-preschool", "学前2岁"),
                            ("age3-preschool", "学前3岁"),
                            ("age4-preschool", "学前4岁"),
                            ("age5-preschool", "学前5岁"),
                            ("kindergarten", "幼儿园"),
                            ("grade1-primary", "小学一年级"),
                            ("grade2-primary", "小学二年级"),
                            ("grade3-primary", "小学三年级"),
                            ("grade4-primary", "小学四年级"),
                            ("grade5-primary", "小学五年级"),
                            ("grade6-primary", "小学六年级"),
                            ("grade7-middle", "初中一年级"),
                            ("grade8-middle", "初中二年级"),
                            ("grade9-middle", "初中三年级"),
                            ("grade10-high", "高中一年级"),
                            ("grade11-high", "高中二年级"),
                            ("grade12-high", "高中三年级"),
                            ("freshman-university", "大学一年级"),
                            ("sophomore-university", "大学二年级"),
                            ("junior-university", "大学三年级"),
                            ("senior-university", "大学四年级"),
                        ],
                        default="1t2-preschool",
                        max_length=30,
                        verbose_name="年级",
                    ),
                ),
                ("pic_style", models.CharField(default="realistic", max_length=20, verbose_name="图片风格")),
                ("utime", models.DateTimeField(auto_now=True)),
                (
                    "illustration",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="pic_book.illustrationfile"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_knowledge_point",
                "unique_together": {("knowledge_uniq", "pic_style", "language")},
            },
        ),
        migrations.CreateModel(
            name="VoiceTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("title", models.CharField(max_length=500, verbose_name="标题")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en_US", "英语"),
                            ("zh_CN", "简体中文"),
                            ("fr_FR", "法语"),
                            ("es_ES", "西班牙语"),
                            ("ar_AE", "阿拉伯语"),
                            ("ru_RU", "俄语"),
                            ("pt_BR", "葡萄牙语"),
                            ("ja_JP", "日语"),
                            ("de_DE", "德语"),
                            ("ko_KR", "韩语"),
                            ("in_ID", "印尼语"),
                            ("ms_MY", "马来语"),
                            ("th_TH", "泰语"),
                            ("hi_IN", "北印度语"),
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
                        ],
                        default="en_US",
                        max_length=16,
                        verbose_name="语言",
                    ),
                ),
                ("speaker", models.CharField(blank=True, max_length=50, verbose_name="语音文件")),
                ("tts_model", models.CharField(default="coqui-xld1", max_length=20, verbose_name="使用tts模型")),
                ("utime", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_voice_template",
            },
        ),
        migrations.CreateModel(
            name="PicBook",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("title", models.CharField(max_length=500, verbose_name="标题")),
                ("description", models.CharField(blank=True, max_length=1000, null=True, verbose_name="描述信息")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en_US", "英语"),
                            ("zh_CN", "简体中文"),
                            ("fr_FR", "法语"),
                            ("es_ES", "西班牙语"),
                            ("ar_AE", "阿拉伯语"),
                            ("ru_RU", "俄语"),
                            ("pt_BR", "葡萄牙语"),
                            ("ja_JP", "日语"),
                            ("de_DE", "德语"),
                            ("ko_KR", "韩语"),
                            ("in_ID", "印尼语"),
                            ("ms_MY", "马来语"),
                            ("th_TH", "泰语"),
                            ("hi_IN", "北印度语"),
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
                        ],
                        default="en_US",
                        max_length=16,
                        verbose_name="语言",
                    ),
                ),
                (
                    "language_level",
                    models.CharField(
                        choices=[
                            ("A1", "入门级，可以做简单的互动与交流"),
                            ("A2", "基础级，能理解并使用熟悉的日常表达法，基本词汇以求满足具体的需求"),
                            ("B1", "进阶级，能理解大部分日常生活中常用句子和表达法"),
                            ("B2", "高阶级，能在与以目标语言为母语的对象做互动时保持一定流畅度"),
                            ("C1", "流利运用级，在社交上、学术上及专业的场合中，皆能灵活的有效地运用语言资源"),
                            ("C2", "精通级，能流利、准确、并即兴的表达自己的意见，并且在较为复杂的情况下亦能有效地表达或区别出言外之意"),
                        ],
                        default="A1",
                        max_length=16,
                        verbose_name="语言级别",
                    ),
                ),
                (
                    "phase",
                    models.CharField(
                        choices=[
                            ("preschool", "学前班"),
                            ("kindergarten", "幼儿园"),
                            ("primary", "小学"),
                            ("middle", "初中"),
                            ("high", "高中"),
                            ("university", "大学"),
                        ],
                        default="preschool",
                        max_length=20,
                        verbose_name="学段",
                    ),
                ),
                (
                    "grade",
                    models.CharField(
                        choices=[
                            ("age1-preschool", "学前1岁"),
                            ("age2-preschool", "学前2岁"),
                            ("age3-preschool", "学前3岁"),
                            ("age4-preschool", "学前4岁"),
                            ("age5-preschool", "学前5岁"),
                            ("kindergarten", "幼儿园"),
                            ("grade1-primary", "小学一年级"),
                            ("grade2-primary", "小学二年级"),
                            ("grade3-primary", "小学三年级"),
                            ("grade4-primary", "小学四年级"),
                            ("grade5-primary", "小学五年级"),
                            ("grade6-primary", "小学六年级"),
                            ("grade7-middle", "初中一年级"),
                            ("grade8-middle", "初中二年级"),
                            ("grade9-middle", "初中三年级"),
                            ("grade10-high", "高中一年级"),
                            ("grade11-high", "高中二年级"),
                            ("grade12-high", "高中三年级"),
                            ("freshman-university", "大学一年级"),
                            ("sophomore-university", "大学二年级"),
                            ("junior-university", "大学三年级"),
                            ("senior-university", "大学四年级"),
                        ],
                        default="age2-preschool",
                        max_length=30,
                        verbose_name="年级",
                    ),
                ),
                (
                    "cover_img",
                    models.ImageField(blank=True, max_length=500, null=True, upload_to="", verbose_name="封面图"),
                ),
                ("utime", models.DateTimeField(auto_now=True)),
                ("author", models.ManyToManyField(to="users.author")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_pic_books",
            },
        ),
        migrations.CreateModel(
            name="ChapterTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("title", models.CharField(max_length=500, verbose_name="标题")),
                ("description", models.CharField(blank=True, max_length=1000, null=True, verbose_name="描述信息")),
                (
                    "c_type",
                    models.CharField(
                        choices=[("public", "完全公开"), ("protected", "内部使用"), ("private", "私人&平台不可用")],
                        default="protected",
                        help_text="public完全公开共享；protected内置受保护，仅平台可用；private私人创建，平台和其他人不可用",
                        max_length=16,
                        verbose_name="章节类型",
                    ),
                ),
                ("text_template", models.TextField(blank=True, verbose_name="文案模板")),
                (
                    "grid_layout",
                    models.CharField(help_text="单页面内图片，1*1, 2*2, 3*3, 2*4布局", max_length=200, verbose_name="栅格布局"),
                ),
                ("font_color", models.CharField(max_length=500, verbose_name="颜色")),
                ("font_family", models.CharField(max_length=500, verbose_name="字体")),
                ("font_size", models.CharField(max_length=500, verbose_name="文字大小")),
                ("background_img", models.ImageField(max_length=500, upload_to="", verbose_name="背景图面")),
                ("background_color", models.ImageField(max_length=500, upload_to="", verbose_name="背景颜色")),
                (
                    "text_position",
                    models.CharField(
                        default="bottom", help_text="文本框在图片中的位置：上中下左右？", max_length=20, verbose_name="文本位置"
                    ),
                ),
                (
                    "text_opacity",
                    models.FloatField(
                        default=1, help_text="opacity为不透度度，1为完全显示，0为完全透明; 0.5为半透明 ", verbose_name="文本透明度"
                    ),
                ),
                ("utime", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "voice_template",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pic_book.voicetemplate"),
                ),
            ],
            options={
                "db_table": "mlnbook_pic_book_chapter_template",
            },
        ),
        migrations.CreateModel(
            name="BookSeries",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("title", models.CharField(max_length=500, verbose_name="标题")),
                ("description", models.CharField(blank=True, max_length=1000, null=True, verbose_name="描述信息")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en_US", "英语"),
                            ("zh_CN", "简体中文"),
                            ("fr_FR", "法语"),
                            ("es_ES", "西班牙语"),
                            ("ar_AE", "阿拉伯语"),
                            ("ru_RU", "俄语"),
                            ("pt_BR", "葡萄牙语"),
                            ("ja_JP", "日语"),
                            ("de_DE", "德语"),
                            ("ko_KR", "韩语"),
                            ("in_ID", "印尼语"),
                            ("ms_MY", "马来语"),
                            ("th_TH", "泰语"),
                            ("hi_IN", "北印度语"),
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
                        ],
                        default="en_US",
                        max_length=16,
                        verbose_name="语言",
                    ),
                ),
                ("share_state", models.CharField(default="public", max_length=16, verbose_name="公开状态")),
                ("utime", models.DateTimeField(auto_now=True)),
                ("pic_books", models.ManyToManyField(to="pic_book.picbook")),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_book_series",
            },
        ),
        migrations.CreateModel(
            name="ParagraphVoiceFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                (
                    "para_content_uniq",
                    models.CharField(help_text="content文本MD5加密", max_length=64, verbose_name="段落内容唯一标识"),
                ),
                ("voice_file", models.FileField(upload_to="pic_book/voice_file", verbose_name="语音文件")),
                ("duration", models.IntegerField(default=1000, verbose_name="毫秒")),
                ("utime", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "voice_template",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pic_book.voicetemplate"),
                ),
            ],
            options={
                "db_table": "mlnbook_pic_book_paragraph_voice_file",
                "unique_together": {("para_content_uniq", "voice_template")},
            },
        ),
        migrations.CreateModel(
            name="Paragraph",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                ("para_content", models.TextField(help_text="段落内容；一般基于知识点+章节复合生成", verbose_name="段落内容")),
                (
                    "para_content_uniq",
                    models.CharField(help_text="content文本MD5加密", max_length=64, verbose_name="段落内容唯一标识"),
                ),
                ("page_num", models.IntegerField(default=1, verbose_name="页码")),
                ("page_para_seq", models.IntegerField(default=1, verbose_name="页内段落排序")),
                ("utime", models.DateTimeField(auto_now=True)),
                (
                    "chapter",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pic_book.chaptertemplate"),
                ),
                (
                    "illustration",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="pic_book.illustrationfile"
                    ),
                ),
                (
                    "knowledge_point",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="pic_book.knowledgepoint"
                    ),
                ),
                ("pic_book", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pic_book.picbook")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "mlnbook_pic_book_paragraph",
                "unique_together": {("pic_book", "chapter", "para_content_uniq")},
            },
        ),
        migrations.CreateModel(
            name="KnowledgeVoiceFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ctime", models.DateTimeField(auto_created=True)),
                (
                    "knowledge_uniq",
                    models.CharField(help_text="content文本MD5加密", max_length=64, verbose_name="知识点唯一标识"),
                ),
                ("voice_file", models.FileField(upload_to="pic_book/voice_file", verbose_name="语音文件")),
                ("duration", models.IntegerField(default=1000, verbose_name="毫秒")),
                ("utime", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "voice_template",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pic_book.voicetemplate"),
                ),
            ],
            options={
                "db_table": "mlnbook_pic_book_knowledge_voice_file",
                "unique_together": {("knowledge_uniq", "voice_template")},
            },
        ),
    ]
