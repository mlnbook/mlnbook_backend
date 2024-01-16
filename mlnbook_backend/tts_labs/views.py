# coding=utf-8
from rest_framework import viewsets, status
from rest_framework.response import Response

from mlnbook_backend.tts_labs.models import TTSJobInstance
from mlnbook_backend.tts_labs.serializers import TTSJobInstanceSerializer
from mlnbook_backend.tts_labs.tts_connector.azure_microsoft_sdk import azure_tts
from mlnbook_backend.tts_labs.tts_connector.elevenlabs_sdk import elevenlab_tts


# Create your views here.
class TTSJobViewSet(viewsets.ModelViewSet):
    queryset = TTSJobInstance.objects.all()
    serializer_class = TTSJobInstanceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # tts 服务调用
        tts_cfg = {"azure-api": azure_tts, "elevenlab": elevenlab_tts}
        tts_model = request.data.get("tts_model", "azure-api")
        req_txt = request.data.get("req_txt")
        req_type = request.data.get("req_type")
        voice_file = tts_cfg[tts_model](req_txt, req_type)
        instance.voice_file = voice_file
        instance.duration = voice_file
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
