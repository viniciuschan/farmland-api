from rest_framework.routers import DefaultRouter

from src.views import FarmerViewSet, FarmViewSet, LocationViewSet

router = DefaultRouter()
router.register(r"farmers", FarmerViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"farms", FarmViewSet)

urlpatterns = router.urls
