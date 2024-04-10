from rest_framework.routers import DefaultRouter

from api.views import ReadDiaryViewSet, ReadNoteViewSet

router = DefaultRouter()
router.register("diaries", ReadDiaryViewSet, basename="diaries")
router.register("notes", ReadNoteViewSet, basename="notes")
