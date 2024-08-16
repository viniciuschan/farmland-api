import pytest

from src.models import Farm, Farmer, Location


@pytest.fixture
def mock_farm_data():
    yield {
        "name": "Yellowstone Farm",
        "total_area_hectares": 150,
        "cultivable_area_hectares": 120,
        "vegetation_area_hectares": 30,
        "cultivations": ["SOY"],
        "farmer": {
            "username": "John Dunha",
            "document_type": "CPF",
            "document_value": "747.449.360-83",
        },
        "location": {
            "city": "Rio de Janeiro",
            "state": "RJ",
        },
    }


@pytest.fixture
def mock_farmer(mock_farm_data):
    yield Farmer.objects.create(
        username=mock_farm_data["farmer"]["username"],
        document_type=mock_farm_data["farmer"]["document_type"],
        document_value=mock_farm_data["farmer"]["document_value"],
    )


@pytest.fixture
def mock_location(mock_farm_data):
    yield Location.objects.create(
        city=mock_farm_data["location"]["city"],
        state=mock_farm_data["location"]["state"],
    )


@pytest.fixture
def mock_farm(mock_farm_data, mock_farmer, mock_location):
    yield Farm.objects.create(
        farmer=mock_farmer,
        location=mock_location,
        name=mock_farm_data["name"],
        total_area_hectares=mock_farm_data["total_area_hectares"],
        cultivable_area_hectares=mock_farm_data["cultivable_area_hectares"],
        vegetation_area_hectares=mock_farm_data["vegetation_area_hectares"],
        cultivations=mock_farm_data["cultivations"],
    )
