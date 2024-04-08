from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
]


admin.site.site_header = "Diary API"
admin.site.site_title = "Diary API"
admin.site.index_title = "Welcome to Diary API"
