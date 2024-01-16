# coding=utf-8
import hashlib
from django.db import models
from django.conf import settings

from mlnbook_backend.utils.global_choices import AZURE_VOICE_STYLE

REQUEST_CONTENT_CHOICES = (
    ('txt', 'txt'),
    ('ssml', 'ssml'),
)


class TTSJobInstance(models.Model):
    c_type = models.CharField("类型", max_length=16, default="schedule", help_text="temporary or schedule")
    language = models.CharField("语言", max_length=16, default="en_US", help_text="language-ios_code, coqui保存路径")
    tts_model = models.CharField("tts模型", max_length=20, default="azure-api",
                                 help_text="开源TTS算法 coqui-ai, 微软语音服务 azure-api")
    voice_name = models.CharField("主语音编码", max_length=100, blank=True, null=True)
    style = models.CharField("说话风格", blank=True, null=True, choices=AZURE_VOICE_STYLE)
    pitch = models.SmallIntegerField("音调", default=0, help_text="最大+50%，最小-50%")
    rate = models.SmallIntegerField("语速", default=0, help_text="最大+200%，最小-100%")
    # volume = models.SmallIntegerField("音量", default=100, help_text="最大100，最小0")
    req_ssml = models.TextField("请求文本", help_text="ssml或纯文本")
    job_state = models.SmallIntegerField("任务状态", default=0)
    job_detail = models.TextField("任务执行信息", blank=True)
    voice_file = models.FileField("语音文件", upload_to="pic_book/voice_file", null=True, blank=True)
    duration = models.IntegerField("毫秒", default=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mlnbook_tts_labs_job_instances"

    def __str__(self):
        return self.voice_file.url
