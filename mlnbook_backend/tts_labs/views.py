# coding=utf-8
from rest_framework import viewsets, status

from mlnbook_backend.tts_labs.models import TTSJobInstance
from mlnbook_backend.tts_labs.serializers import TTSJobInstanceSerializer


# Create your views here.
class TTSJobViewSet(viewsets.ModelViewSet):
    queryset = TTSJobInstance.objects.all()
    serializer_class = TTSJobInstanceSerializer
