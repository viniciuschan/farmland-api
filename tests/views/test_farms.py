import pytest
from django.urls import reverse
from rest_framework import status

from src.models import Farm, Farmer, Location


def test_farms_url():
    url = reverse("farms-list")
    assert url == "/api/farms/"


@pytest.mark.django_db
def test_create_farm(mock_client, mock_farm_data, mock_farmer_data, mock_location_data):
    url = reverse("farms-list")

    mock_farm_data["farmer"] = mock_farmer_data
    mock_farm_data["location"] = mock_location_data

    response = mock_client.post(url, mock_farm_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    farm = Farm.objects.get(id=response.data["id"])
    assert farm.name == "Yellowstone Farm"

    assert Farmer.objects.count() == 1
    assert Location.objects.count() == 1


@pytest.mark.django_db
def test_get_farm(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
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
def test_list_farms(mock_client, mock_farm):
    url = reverse("farms-list")
    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
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
    ]


@pytest.mark.django_db
def test_partial_update_farm(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    data = {"name": "Updated Farm"}
    response = mock_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    mock_farm.refresh_from_db()
    assert mock_farm.name == "Updated Farm"


@pytest.mark.django_db
def test_update_farm(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    data = {
        "name": "Updated Farm",
        "total_area_hectares": 500,
        "cultivable_area_hectares": 250,
        "vegetation_area_hectares": 250,
        "cultivations": ["CORN", "COTTON"],
        "farmer": {
            "username": "John Updated",
            "document_type": "CNPJ",
            "document_value": "14.963.945/0001-13",
        },
        "location": {
            "city": "Manaus",
            "state": "AM",
        },
    }
    response = mock_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    mock_farm.refresh_from_db()
    assert mock_farm.name == "Updated Farm"
    assert mock_farm.total_area_hectares == 500
    assert mock_farm.cultivable_area_hectares == 250
    assert mock_farm.vegetation_area_hectares == 250
    assert mock_farm.cultivations == ["CORN", "COTTON"]
    assert mock_farm.farmer.username == "John Updated"
    assert mock_farm.farmer.document_type == "CNPJ"
    assert mock_farm.farmer.document_value == "14963945000113"
    assert mock_farm.location.city == "Manaus"
    assert mock_farm.location.state == "AM"


@pytest.mark.django_db
def test_delete_farm(mock_client, mock_farm):
    url = reverse("farms-detail", args=[mock_farm.id])
    response = mock_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(Farm.DoesNotExist):
        mock_farm.refresh_from_db()


@pytest.mark.django_db
@pytest.mark.usefixtures("mock_farm", "mock_another_farms")
def test_farm_dashboard(mock_client):
    url = reverse("farms-dashboard")
    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "total_farms": {
            "count": 4,
            "area": {"total": "600.00", "cultivation": "480.00", "vegetation": "120.00"},
        },
        "farms_per_state": {
            "SP": {"total_count": 1, "total_area": "150.00"},
            "RJ": {"total_count": 1, "total_area": "150.00"},
            "GO": {"total_count": 1, "total_area": "150.00"},
            "MT": {"total_area": "150.00", "total_count": 1},
        },
        "total_farms_per_cultivation": {
            "CORN": {"percentage": "0.2", "total_farms": 1},
            "COTTON": {"percentage": "0.2", "total_farms": 1},
            "SOY": {"percentage": "0.4", "total_farms": 2},
            "SUGAR_CANE": {"percentage": "0.2", "total_farms": 1},
        },
    }


@pytest.mark.django_db
def test_farm_dashboard_with_empty_data(mock_client):
    url = reverse("farms-dashboard")
    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "farms_per_state": {},
        "total_farms": {
            "area": {
                "cultivation": "0.00",
                "total": "0.00",
                "vegetation": "0.00",
            },
            "count": 0,
        },
        "total_farms_per_cultivation": {},
    }
