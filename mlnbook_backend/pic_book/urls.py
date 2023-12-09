# coding=utf-8
from django.urls import path, include
from rest_framework import routers

from mlnbook_backend.pic_book.views import PicBookViewSet

router = routers.DefaultRouter()
router.register('pic_book', PicBookViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = router.urls
