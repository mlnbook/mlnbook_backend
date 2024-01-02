# coding=utf-8
from rest_framework import serializers

from mlnbook_backend.users.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'description', 'c_type', 'language', 'utime']
