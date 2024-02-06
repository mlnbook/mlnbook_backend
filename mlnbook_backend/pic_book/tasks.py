# coding=utf-8
import base64
import logging
from django.conf import settings
from config import celery_app

from django.core.files.base import ContentFile

from mlnbook_backend.aigc_labs.aigc_connector.stable_diffusion_api import call_txt2img_api
from mlnbook_backend.pic_book.models import ParagraphVoiceFile, Chapter, Paragraph
from mlnbook_backend.tts_labs.tts_connector.azure_microsoft_sdk import azure_tts
from mlnbook_backend.utils.img_resize import image_resize


@celery_app.task()
def paragraph_voice_file_task(pic_book_id, voice_template_id):
    queryset = ParagraphVoiceFile.objects.filter(pic_book_id=pic_book_id, voice_template_id=voice_template_id)
    # 调用tts api接口
    for item in queryset:
        try:
            audio_data = azure_tts(item.para_ssml, item.voice_template.language, item.voice_template.voice_name)
            file_data = ContentFile(audio_data)
            item.job_state = 1
            item.voice_file.save("voice_%s.wav" % item.para_content_uniq, file_data)
        except Exception as e:
            item.job_state = 0
            item.job_detail = str(e)
            item.save()


@celery_app.task()
def paragraph_aigc_image_task(chapter_id):
    chapter_obj = Chapter.objects.get(id=chapter_id)
    # 仅处理没有上传过图片的；已上传的需要人工手动修改
    queryset = Paragraph.objects.filter(chapter=chapter_obj, illustration="")
    for para_obj in queryset:
        print(para_obj.para_content)
        payload = {"prompt": para_obj.aigc_prompt}
        aigc_img = call_txt2img_api(payload)
        if not aigc_img:
            return
        illustration_img = image_resize(aigc_img, size=(512, 512), opened=True)
        small_img = image_resize(aigc_img, size=(80, 80), opened=True)
        para_obj.illustration = illustration_img
        para_obj.small_illustration = small_img
        para_obj.save()
