# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.pic_book.models import PicBook, BookSeries


class PicBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicBook
        fields = ['id', 'title', 'description', 'language', 'language_level', 'phase', 'grade', 'author', 'utime']


class BookSeriesListSerializer(serializers.ModelSerializer):
    pic_books = PicBookSerializer(many=True, read_only=True)

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']


class BookSeriesCreateSerializer(serializers.ModelSerializer):
    pic_books = serializers.PrimaryKeyRelatedField(many=True, queryset=PicBook.objects.all())

    class Meta:
        model = BookSeries
        fields = ['id', 'title', 'description', 'language', 'utime', 'pic_books']
