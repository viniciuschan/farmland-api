from decimal import Decimal

import pytest

from src.models import Farm, Farmer, Location


@pytest.mark.django_db
@pytest.mark.freeze_time("2024-08-16 00:00:00")
def test_farmer_model(mock_farmer_data):
    clean_document_value = "74744936083"

    instance = Farmer.objects.create(**mock_farmer_data)
    assert instance.username == "John Dunha"
    assert instance.document_type == "CPF"
    assert instance.document_value == clean_document_value
    assert str(instance.created_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance.updated_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance) == "John Dunha"

    assert Farmer.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time("2024-08-16 00:00:00")
def test_location_model(mock_location_data):
    instance = Location.objects.create(**mock_location_data)
    assert instance.city == "Rio de Janeiro"
    assert instance.state == "RJ"
    assert str(instance.created_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance.updated_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance) == "RJ - Rio de Janeiro"

    assert Location.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.freeze_time("2024-08-16 00:00:00")
def test_farm_model(mock_farm_data, mock_farmer, mock_location):
    mock_farm_data["farmer"] = mock_farmer
    mock_farm_data["location"] = mock_location

    instance = Farm.objects.create(**mock_farm_data)
    assert instance.name == "Yellowstone Farm"
    assert instance.total_area_hectares == Decimal("150.00")
    assert instance.cultivable_area_hectares == Decimal("120.00")
    assert instance.vegetation_area_hectares == Decimal("30.00")
    assert instance.cultivations == ["SOY"]
    assert str(instance.created_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance.updated_at) == "2024-08-16 00:00:00+00:00"
    assert str(instance) == "Yellowstone Farm"
    assert str(instance.farmer) == "John Dunha"
    assert str(instance.location) == "RJ - Rio de Janeiro"

    assert Farm.objects.count() == 1
    assert Farmer.objects.count() == 1
    assert Location.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("mock_farm", "mock_another_farms")
def test_farmer_model_total_farms_data():
    result = Farm.objects.total_farms_data()
    assert result == {
        "total_cultivable_area": "480.00",
        "total_farms_area": "600.00",
        "total_farms_count": 4,
        "total_vegetation_area": "120.00",
    }


@pytest.mark.django_db
@pytest.mark.usefixtures("mock_farm", "mock_another_farms")
def test_farmer_model_farms_per_state():
    result = Farm.objects.farms_per_state()
    assert result == {
        "GO": {"total_area": "150.00", "total_count": 1},
        "MT": {"total_area": "150.00", "total_count": 1},
        "RJ": {"total_area": "150.00", "total_count": 1},
        "SP": {"total_area": "150.00", "total_count": 1},
    }


@pytest.mark.django_db
@pytest.mark.usefixtures("mock_farm", "mock_another_farms")
def test_farmer_model_farms_per_cultivation():
    result = Farm.objects.farms_per_cultivation()
    assert result == {
        "CORN": {"total_cultivable_area": "240.00", "total_farms": 2},
        "COTTON": {"total_cultivable_area": "120.00", "total_farms": 1},
        "SOY": {"total_cultivable_area": "240.00", "total_farms": 2},
        "SUGAR_CANE": {"total_cultivable_area": "120.00", "total_farms": 1},
    }
