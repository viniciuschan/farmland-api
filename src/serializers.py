import bleach
from rest_framework import serializers

from src.constants import BrazilianState
from src.models import Farm, Farmer, Location
from src.validators import DocumentValidator


def clean_doc_characters(value: str) -> str:
    doc_number = value.replace(".", "").replace("-", "").replace("/", "")
    return doc_number.strip()


def sanitize_data(value: str) -> str:
    cleaner = bleach.Cleaner(tags=[], strip=True, strip_comments=True)
    return cleaner.clean(value).strip()


class FarmerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    document_value = serializers.CharField(max_length=18)

    def validate_username(self, value: str):
        return sanitize_data(value)

    def validate(self, data: dict):
        data = super().validate(data)
        document_type = data.get("document_type")
        cleaned_document_value = clean_doc_characters(data.get("document_value"))
        data["document_value"] = cleaned_document_value

        validator = DocumentValidator(document_type)
        if not validator.validate(cleaned_document_value):
            raise serializers.ValidationError("Invalid document")

        return data

    class Meta:
        model = Farmer
        fields = (
            "username",
            "document_type",
            "document_value",
        )


class LocationSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=2)

    def validate_city(self, value):
        if not value:
            raise serializers.ValidationError("City cannot be empty")
        return sanitize_data(value)

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError("State cannot be empty")

        if value not in [item.name for item in BrazilianState]:
            raise serializers.ValidationError("Invalid state")

        return value

    class Meta:
        model = Location
        fields = (
            "city",
            "state",
        )


class FarmSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer()
    location = LocationSerializer()

    def validate(self, data: dict) -> dict:
        data = super().validate(data)

        # dont forget: farm area validations
        return data

    def create(self, validated_data: dict):
        farmer_data = validated_data.pop("farmer")
        location_data = validated_data.pop("location")

        farmer, _ = Farmer.objects.get_or_create(**farmer_data)
        location, _ = Location.objects.get_or_create(**location_data)

        farm = Farm.objects.create(farmer=farmer, location=location, **validated_data)
        return farm

    def update(self, instance: Farm, validated_data: dict):
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
