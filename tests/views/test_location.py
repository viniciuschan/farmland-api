import pytest
from django.urls import reverse
from rest_framework import status

from src.models import Location


@pytest.mark.django_db
def test_create_location(mock_client, mock_location_data):
    url = reverse("locations-list")
    response = mock_client.post(url, mock_location_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    assert Location.objects.count() == 1
    location = Location.objects.get(id=response.data["id"])
    assert location.city == "Rio de Janeiro"
    assert location.state == "RJ"


@pytest.mark.django_db
def test_retrieve_location(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])

    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": str(mock_location.id),
        "city": "Rio de Janeiro",
        "state": "RJ",
    }


@pytest.mark.django_db
def test_list_locations(mock_client, mock_location):
    url = reverse("locations-list")

    response = mock_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "id": str(mock_location.id),
            "city": "Rio de Janeiro",
            "state": "RJ",
        }
    ]


@pytest.mark.django_db
def test_partial_update_location(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    data = {"city": "Updated City"}
    response = mock_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    mock_location.refresh_from_db()
    assert mock_location.city == "Updated City"


@pytest.mark.django_db
def test_update_location(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    data = {"city": "Updated City", "state": "SP"}
    response = mock_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    mock_location.refresh_from_db()
    assert mock_location.city == "Updated City"
    assert mock_location.state == "SP"


@pytest.mark.django_db
def test_delete_location(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    response = mock_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(Location.DoesNotExist):
        mock_location.refresh_from_db()
