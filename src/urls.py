from rest_framework.routers import DefaultRouter

from src.views import FarmerViewSet, FarmViewSet, LocationViewSet

router = DefaultRouter()
router.register(r"farmers", FarmerViewSet, basename="farmers")
router.register(r"locations", LocationViewSet, basename="locations")
router.register(r"farms", FarmViewSet, basename="farms")

urlpatterns = router.urls
