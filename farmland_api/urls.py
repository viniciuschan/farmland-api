from django.conf.urls import include
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

ping_view = lambda request: HttpResponse("pong!")

urlpatterns = [
    path("", include("src.urls")),
    path("admin/", admin.site.urls),
    path("ping/", ping_view),
]
