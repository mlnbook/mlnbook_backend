# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from PIL import Image
from io import BytesIO

# from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(ori_image, size=(80,80)):
    # 打开图像
    img = Image.open(ori_image).copy()
    # 调整图像大小
    img.thumbnail(size)
    # 保存到临时内存中
    temp = BytesIO()
    img_suffix = Path(ori_image.name).name.split(".")[-1]
    img_format = image_types[img_suffix]
    img.save(temp, format=img_format)
    # 创建新的 ImageField 类型的内容
    temp.seek(0)  # Seek to the beginning of the file after saving
    image_name = ori_image.name  # Original filename
    new_image = ContentFile(temp.read(), name='small_' + image_name)
    return new_image
