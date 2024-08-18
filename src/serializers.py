import bleach
from rest_framework import serializers

from src.constants import BrazilianState, CultivationType
from src.exceptions import InvalidDocumentTypeError
from src.models import Farm, Farmer, Location
from src.validators import DocumentValidator, FarmValidator


def sanitize_data(value: str) -> str:
    cleaner = bleach.Cleaner(tags=[], strip=True, strip_comments=True)
    return cleaner.clean(value).strip()


class FarmerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    document_value = serializers.CharField(max_length=18)

    def validate_username(self, value: str) -> str:
        return sanitize_data(value)

    def validate(self, data: dict) -> dict:
        data = super().validate(data)

        document_type = data.get("document_type")
        document_value = data.get("document_value")

        if document_type or document_value:
            # If I want update a doc for some reason, I need to provide both fields
            try:
                validator = DocumentValidator(document_type)
            except InvalidDocumentTypeError:
                raise serializers.ValidationError("Invalid document type")

            if not validator.validate(document_value):
                raise serializers.ValidationError("Invalid document value")

            data["document_value"] = validator.clean_punctuations(document_value)

        return data

    class Meta:
        model = Farmer
        fields = (
            "id",
            "username",
            "document_type",
            "document_value",
        )


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=2)

    def validate_city(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("City cannot be empty")
        return sanitize_data(value)

    def validate_state(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("State cannot be empty")

        if value not in [item.name for item in BrazilianState]:
            raise serializers.ValidationError("Invalid state")

        return value

    class Meta:
        model = Location
        fields = (
            "id",
            "city",
            "state",
        )


class FarmSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer()
    location = LocationSerializer()
    cultivations = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate_cultivations(self, value: list) -> list:
        if not value:
            raise serializers.ValidationError("Cultivations cannot be empty")

        cultivations = set([item.upper() for item in value])
        if not cultivations.issubset([item.name for item in CultivationType]):
            raise serializers.ValidationError("Invalid cultivations")

        return list(sorted(cultivations))

    def validate(self, data: dict) -> dict:
        data = super().validate(data)
        total_area = data.get("total_area_hectares")
        cultivable_area = data.get("cultivable_area_hectares")
        vegetation_area = data.get("vegetation_area_hectares")

        # I'm assuming that the farm areas can be updated only if both 3 attrs are present
        if all(
            [
                total_area is not None,
                cultivable_area is not None,
                vegetation_area is not None,
            ]
        ):
            validator = FarmValidator(data)
            if not validator.validate_areas():
                raise serializers.ValidationError("Invalid areas")

        return data

    def create(self, validated_data: dict) -> Farm:
        farmer_data = validated_data.pop("farmer")
        location_data = validated_data.pop("location")

        farmer, _ = Farmer.objects.get_or_create(**farmer_data)
        location, _ = Location.objects.get_or_create(**location_data)

        farm = Farm.objects.create(farmer=farmer, location=location, **validated_data)
        return farm

    def update(self, instance: Farm, validated_data: dict) -> Farm:
        farmer_data = validated_data.pop("farmer", None)
        location_data = validated_data.pop("location", None)

        if farmer_data:
            farmer, _ = Farmer.objects.get_or_create(**farmer_data)
            instance.farmer = farmer

        if location_data:
            location, _ = Location.objects.get_or_create(**location_data)
            instance.location = location

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = Farm
        fields = (
            "id",
            "name",
            "total_area_hectares",
            "cultivable_area_hectares",
            "vegetation_area_hectares",
            "cultivations",
            "farmer",
            "location",
        )
