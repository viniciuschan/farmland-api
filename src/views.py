from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.models import Farm, Farmer, Location
from src.serializers import FarmerSerializer, FarmSerializer, LocationSerializer


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request, *args, **kwargs):
        # Total amount of farms
        # Total farms in hectares (total area)
        # Pie chart by land use (Agricultural area and vegetation)
        total_farms = Farm.objects.total_farms_data()

        # Pie chart by state
        farms_per_state = Farm.objects.farms_per_state()

        # Pie chart by cultivation
        farms_per_cultivation = Farm.objects.farms_per_cultivation()

        data = {
            "total_farms": {
                "count": total_farms["total_farms_count"],
                "area": {
                    "total": total_farms["total_farms_area"],
                    "cultivation": total_farms["total_cultivable_area"],
                    "vegetation": total_farms["total_vegetation_area"],
                },
            },
            "farms_per_state": farms_per_state,
            "farms_per_cultivation": farms_per_cultivation,
        }

        return Response(data, status.HTTP_200_OK)
