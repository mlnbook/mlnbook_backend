# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.tts_labs.models import TTSJobInstance
from mlnbook_backend.utils.base_serializer import AuthModelSerializer


class TTSJobInstanceSerializer(AuthModelSerializer):

    class Meta:
        model = TTSJobInstance
        fields = ['id', 'title', 'language', 'tts_model', 'speaker', 'model_name', 'dataset', 'vocoder',
                  'extra_params', 'req_txt', 'job_state', 'job_state', 'job_detail', 'voice_file',
                  'duration', 'ctime', 'utime']
