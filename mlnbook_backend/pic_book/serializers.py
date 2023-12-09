# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.pic_book.models import PicBook


class PicBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicBook
        fields = ['id', 'title', 'description', 'language']
