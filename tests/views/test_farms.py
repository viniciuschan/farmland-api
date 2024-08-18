import pytest
from django.urls import reverse

from src.models import Farm, Farmer, Location


@pytest.mark.django_db
def test_farm_create(mock_client, mock_farm_data, mock_farmer_data, mock_location_data):
    url = reverse("farms-list")

    mock_farm_data["farmer"] = mock_farmer_data
    mock_farm_data["location"] = mock_location_data

    response = mock_client.post(url, mock_farm_data, format="json")
    assert response.status_code == 201

    assert Farm.objects.count() == 1
    assert Farmer.objects.count() == 1
    assert Location.objects.count() == 1


@pytest.mark.django_db
def test_farm_retrieve(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    response = mock_client.get(url)
    assert response.status_code == 200
    assert response.data == {
        "id": str(mock_farm.id),
        "name": "Yellowstone Farm",
        "total_area_hectares": "150.00",
        "cultivable_area_hectares": "120.00",
        "vegetation_area_hectares": "30.00",
        "cultivations": ["SOY"],
        "farmer": {
            "id": str(mock_farm.farmer.id),
            "username": "John Dunha",
            "document_type": "CPF",
            "document_value": "74744936083",
        },
        "location": {
            "id": str(mock_farm.location.id),
            "city": "Rio de Janeiro",
            "state": "RJ",
        },
    }


@pytest.mark.django_db
def test_farm_partial_update(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    data = {"name": "Updated Farm"}
    response = mock_client.patch(url, data, format="json")
    assert response.status_code == 200

    mock_farm.refresh_from_db()
    assert mock_farm.name == "Updated Farm"


@pytest.mark.django_db
def test_farm_update(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    data = {
        "name": "Updated Farm",
        "total_area_hectares": 500,
        "cultivable_area_hectares": 250,
        "vegetation_area_hectares": 250,
        "cultivations": ["CORN", "COTTON"],
        "farmer": {
            "username": "Jane Dunha",
            "document_type": "CNPJ",
            "document_value": "14.963.945/0001-13",
        },
        "location": {
            "city": "Manaus",
            "state": "AM",
        },
    }
    response = mock_client.put(url, data, format="json")
    assert response.status_code == 200

    mock_farm.refresh_from_db()
    assert mock_farm.name == "Updated Farm"
    assert mock_farm.total_area_hectares == 500
    assert mock_farm.cultivable_area_hectares == 250
    assert mock_farm.vegetation_area_hectares == 250
    assert mock_farm.cultivations == ["CORN", "COTTON"]
    assert mock_farm.farmer.username == "Jane Dunha"
    assert mock_farm.farmer.document_type == "CNPJ"
    assert mock_farm.farmer.document_value == "14963945000113"
    assert mock_farm.location.city == "Manaus"
    assert mock_farm.location.state == "AM"


@pytest.mark.django_db
def test_farm_delete(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    response = mock_client.delete(url)
    assert response.status_code == 204

    with pytest.raises(Farm.DoesNotExist):
        mock_farm.refresh_from_db()
