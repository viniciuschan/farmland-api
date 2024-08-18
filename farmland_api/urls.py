from django.conf.urls import include
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

ping_view = lambda request: HttpResponse("pong!")

urlpatterns = [
    path("", include("src.urls")),
    path("admin/", admin.site.urls),
    path("ping/", ping_view),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
