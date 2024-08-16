import pytest

from src.models import Farm, Farmer, Location


@pytest.fixture
def mock_farmer_data():
    yield {
        "username": "John Dunha",
        "document_type": "CPF",
        "document_value": "747.449.360-83",
    }


@pytest.fixture
def mock_location_data():
    yield {
        "city": "Rio de Janeiro",
        "state": "RJ",
    }


@pytest.fixture
def mock_farm_data(mock_farmer_data, mock_location_data):
    yield {
        "name": "Yellowstone Farm",
        "total_area_hectares": 150,
        "cultivable_area_hectares": 120,
        "vegetation_area_hectares": 30,
        "cultivations": ["SOY"],
        "farmer": mock_farmer_data,
        "location": mock_location_data,
    }


@pytest.fixture
def mock_farmer(mock_farmer_data):
    yield Farmer.objects.create(
        username=mock_farmer_data["username"],
        document_type=mock_farmer_data["document_type"],
        document_value=mock_farmer_data["document_value"],
    )


@pytest.fixture
def mock_location(mock_location_data):
    yield Location.objects.create(
        city=mock_location_data["city"],
        state=mock_location_data["state"],
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
