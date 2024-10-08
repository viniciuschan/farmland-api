import pytest

from src.models import Farm
from src.serializers import FarmerSerializer, FarmSerializer, LocationSerializer, sanitize_data


@pytest.mark.parametrize(
    "input_data, sanitized_data",
    [
        ("<a>(inject-data.com-a)</a>", "(inject-data.com-a)"),
        (" common text no issues.com ", "common text no issues.com"),
        ("'><script>alert(1)", "'&gt;alert(1)"),
        ("Text A (Text B)", "Text A (Text B)"),
        ("<a href=http://inject-url.net>click here", "click here"),
    ],
)
def test_sanitize_data(input_data, sanitized_data):
    assert sanitize_data(input_data) == sanitized_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, expected_username, expected_doc_type, expected_doc_value",
    [
        (
            {"username": "John Doe", "document_type": "CPF", "document_value": "747.449.360-83"},
            "John Doe",
            "CPF",
            "74744936083",
        ),
        (
            {"username": "John Doe", "document_type": "CNPJ", "document_value": "48.542.058/0001-93"},
            "John Doe",
            "CNPJ",
            "48542058000193",
        ),
    ],
)
def test_farmer_serializer_is_valid(data, expected_username, expected_doc_type, expected_doc_value):
    serializer = FarmerSerializer(data=data)
    assert serializer.is_valid() is True
    assert serializer.validated_data["username"] == expected_username
    assert serializer.validated_data["document_type"] == expected_doc_type
    assert serializer.validated_data["document_value"] == expected_doc_value


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        {"username": "John Doe", "document_type": "CPF", "document_value": "invalid-doc"},
        {"username": "John Doe", "document_type": "CNPJ", "document_value": "invalid-doc"},
        {"username": "", "document_type": "CPF", "document_value": "747.449.360-83"},
    ],
)
def test_farmer_serializer_is_not_valid(data):
    serializer = FarmerSerializer(data=data)
    assert serializer.is_valid() is False


@pytest.mark.parametrize(
    "data, expected_city, expected_state",
    [
        ({"city": "Ribeirão Preto", "state": "SP"}, "Ribeirão Preto", "SP"),
        ({"city": "<a href='/evilpath'>Ribeirão Preto</a>", "state": "SP"}, "Ribeirão Preto", "SP"),
    ],
)
def test_location_serializer_is_valid(data, expected_city, expected_state):
    serializer = LocationSerializer(data=data)
    assert serializer.is_valid() is True
    assert serializer.validated_data["city"] == expected_city
    assert serializer.validated_data["state"] == expected_state


@pytest.mark.parametrize(
    "data , invalid_attr",
    [
        ({"city": "", "state": "SP"}, "city"),
        ({"city": "Ribeirão Preto", "state": ""}, "state"),
        ({"city": "Ribeirão Preto", "state": "XX"}, "state"),
    ],
)
def test_location_serializer_is_not_valid(data, invalid_attr):
    serializer = LocationSerializer(data=data)
    assert serializer.is_valid() is False
    assert invalid_attr in serializer.errors


@pytest.mark.django_db
def test_farm_create_serializer_is_valid(mock_farm_data):
    serializer = FarmSerializer(data=mock_farm_data)
    assert serializer.is_valid() is True
    farm = serializer.save()

    instance = Farm.objects.get(name=farm.name)
    assert instance.name == "Yellowstone Farm"
    assert instance.total_area_hectares == 150
    assert instance.cultivable_area_hectares == 120
    assert instance.vegetation_area_hectares == 30
    assert instance.cultivations == ["SOY"]
    assert instance.farmer.username == "John Dunha"
    assert instance.farmer.document_type == "CPF"
    assert instance.farmer.document_value == "74744936083"
    assert instance.farmer.username == "John Dunha"
    assert instance.location.city == "Rio de Janeiro"
    assert instance.location.state == "RJ"


@pytest.mark.django_db
def test_farm_update_serializer_is_valid(mock_farm):
    updated_data = {
        "name": "Updated Farm",
        "total_area_hectares": 500,
        "cultivable_area_hectares": 250,
        "vegetation_area_hectares": 250,
        "cultivations": ["SOY", "CORN", "COTTON"],
        "farmer": {
            "username": "John Dunha",
            "document_type": "CNPJ",
            "document_value": "48542058000193",
        },
        "location": {
            "city": "São Paulo",
            "state": "SP",
        },
    }

    serializer = FarmSerializer(mock_farm, data=updated_data, partial=True)
    assert serializer.is_valid() is True
    farm = serializer.save()

    instance = Farm.objects.get(name=farm.name)
    assert instance.name == updated_data["name"]
    assert instance.cultivations == ["CORN", "COTTON", "SOY"]
    assert instance.total_area_hectares == updated_data["total_area_hectares"]
    assert instance.cultivable_area_hectares == updated_data["cultivable_area_hectares"]
    assert instance.vegetation_area_hectares == updated_data["vegetation_area_hectares"]
    assert instance.farmer.username == updated_data["farmer"]["username"]
    assert instance.farmer.document_type == updated_data["farmer"]["document_type"]
    assert instance.farmer.document_value == updated_data["farmer"]["document_value"]
    assert instance.farmer.username == updated_data["farmer"]["username"]
    assert instance.location.city == updated_data["location"]["city"]
    assert instance.location.state == updated_data["location"]["state"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "total_area, cultivable_area, vegetation_area",
    [
        (0, 50, 50),
        (0, 0, 0),
        (100, 150, -50),
        (100, -50, -150),
    ],
)
def test_farm_serializer_create_with_invalid_areas(
    total_area, cultivable_area, vegetation_area, mock_farm_data
):
    mock_farm_data["total_area_hectares"] = total_area
    mock_farm_data["cultivable_area_hectares"] = cultivable_area
    mock_farm_data["vegetation_area_hectares"] = vegetation_area
    serializer = FarmSerializer(data=mock_farm_data)
    assert serializer.is_valid() is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "cultivations",
    [
        [],
        "INVALID",
        None,
    ],
)
def test_farm_serializer_create_with_invalid_cultivations(cultivations, mock_farm_data):
    mock_farm_data["cultivations"] = cultivations
    serializer = FarmSerializer(data=mock_farm_data)
    assert serializer.is_valid() is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "total_area, cultivable_area, vegetation_area",
    [
        (0, 50, 50),
        (0, 0, 0),
        (100, 150, -50),
        (100, -50, -150),
    ],
)
def test_farm_serializer_update_with_invalid_areas(
    total_area, cultivable_area, vegetation_area, mock_farm_data, mock_farm
):
    mock_farm_data["total_area_hectares"] = total_area
    mock_farm_data["cultivable_area_hectares"] = cultivable_area
    mock_farm_data["vegetation_area_hectares"] = vegetation_area
    serializer = FarmSerializer(mock_farm, data=mock_farm_data)
    assert serializer.is_valid() is False
