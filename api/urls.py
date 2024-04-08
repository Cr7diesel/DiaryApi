from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DiaryView, ReadDiaryViewSet, ReadNoteViewSet, NoteView

router = DefaultRouter()
router.register("diaries", ReadDiaryViewSet)
router.register("notes", ReadNoteViewSet)

urlpatterns = [
    path("diary/create/", DiaryView.as_view(), name="create_diary"),
    path("diary/update/<int:diary_id>/", DiaryView.as_view(), name="update_diary"),
    path("diary/delete/<int:diary_id>/", DiaryView.as_view(), name="delete_diary"),
    path("note/create/", NoteView.as_view(), name="create_note"),
    path("note/update/<int:note_id>/", NoteView.as_view(), name="update_note"),
    path("note/delete/<int:note_id>/", NoteView.as_view(), name="delete_not"),
]

urlpatterns += router.urls
