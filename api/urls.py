from django.urls import path, include

from .routers import router
from .views import (
    CreateDiaryView,
    CreateNoteView,
    CreateUserView,
    UpdateDiaryView,
    DeleteDiaryView,
    UpdateNoteView,
    DeleteNoteView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("diary/create/", CreateDiaryView.as_view(), name="create_diary"),
    path("diary/update/<int:id>/", UpdateDiaryView.as_view(), name="update_diary"),
    path("diary/delete/<int:id>/", DeleteDiaryView.as_view(), name="delete_diary"),
    path("note/create/", CreateNoteView.as_view(), name="create_note"),
    path("note/update/<int:id>/", UpdateNoteView.as_view(), name="update_note"),
    path("note/delete/<int:id>/", DeleteNoteView.as_view(), name="delete_not"),
    path("", include(router.urls)),
]
