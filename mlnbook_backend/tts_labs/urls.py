from rest_framework import routers

from mlnbook_backend.tts_labs.views import TTSJobViewSet

router = routers.DefaultRouter()
router.register('tts_job', TTSJobViewSet)

urlpatterns = router.urls
