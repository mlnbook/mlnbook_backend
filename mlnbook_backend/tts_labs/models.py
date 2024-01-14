# coding=utf-8
import hashlib
from django.db import models
from django.conf import settings


REQUEST_CONTENT_CHOICES = (
    ('txt', 'txt'),
    ('ssml', 'ssml'),
)


class TTSJobInstance(models.Model):
    c_type = models.CharField("类型", max_length=16, default="schedule", help_text="temporary or schedule")
    language = models.CharField("语言", max_length=16, default="en_US", help_text="language-ios_code, coqui保存路径")
    tts_model = models.CharField("tts模型", max_length=20, default="azure-api",
                                 help_text="开源TTS算法 coqui-ai, 微软语音服务 azure-api")
    speaker = models.CharField("语音编码", max_length=50, blank=True, null=True)
    model_name = models.CharField("模型名称", max_length=20, blank=True, null=True, help_text="xtts_v1")
    dataset = models.CharField("模型数据集", max_length=20, blank=True, null=True, help_text="ljspeech")
    vocoder = models.CharField("vocoder", max_length=20, blank=True, null=True, help_text="hifigan_v2")
    extra_params = models.JSONField("语音参数", blank=True, null=True)
    req_txt = models.TextField("请求文本", help_text="ssml或纯文本")
    req_type = models.CharField("请求文本类型", max_length=16, default='txt', choices=REQUEST_CONTENT_CHOICES,
                                help_text="ssml或纯文本")
    content_uniq = models.CharField("内容标识", max_length=64, help_text="请求内容文本MD5加密，例行时段落标识写入")
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
