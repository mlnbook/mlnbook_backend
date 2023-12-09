# coding=utf-8
from rest_framework import viewsets

from mlnbook_backend.pic_book.models import PicBook
from mlnbook_backend.pic_book.serializers import PicBookSerializer


class PicBookViewSet(viewsets.ModelViewSet):
    queryset = PicBook.objects.all()
    serializer_class = PicBookSerializer
