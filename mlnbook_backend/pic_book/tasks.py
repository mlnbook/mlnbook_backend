# coding=utf-8
import base64
import logging
from django.conf import settings
from config import celery_app

from django.core.files.base import ContentFile
from mlnbook_backend.pic_book.models import ParagraphVoiceFile
from mlnbook_backend.tts_labs.tts_connector.azure_microsoft_sdk import azure_tts


@celery_app.task()
def paragraph_voice_file_task(pic_book_id, voice_template_id):
    queryset = ParagraphVoiceFile.objects.filter(pic_book_id=pic_book_id, voice_template_id=voice_template_id)
    # 调用tts api接口
    for item in queryset:
        audio_data = azure_tts(item.para_ssml, item.voice_template.language, item.voice_template.voice_name)
        file_data = ContentFile(base64.b64decode(audio_data))
        item.voice_file.save("voice_%s.wav" % item.para_content_uniq, file_data)
