import pytest
from django.urls import reverse

from src.models import Location


@pytest.mark.django_db
def test_location_create(mock_client, mock_location_data):
    url = reverse("locations-list")
    response = mock_client.post(url, mock_location_data, format="json")
    assert response.status_code == 201

    assert Location.objects.count() == 1
    location = Location.objects.get(id=response.data["id"])
    assert location.city == "Rio de Janeiro"
    assert location.state == "RJ"


@pytest.mark.django_db
def test_location_retrieve(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])

    response = mock_client.get(url)
    assert response.status_code == 200
    assert response.data == {"id": str(mock_location.id), "city": "Rio de Janeiro", "state": "RJ"}


@pytest.mark.django_db
def test_location_partial_update(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    data = {"city": "Updated City"}
    response = mock_client.patch(url, data, format="json")
    assert response.status_code == 200

    mock_location.refresh_from_db()
    assert mock_location.city == "Updated City"


@pytest.mark.django_db
def test_location_update(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    data = {"city": "Updated City", "state": "SP"}
    response = mock_client.put(url, data, format="json")
    assert response.status_code == 200

    mock_location.refresh_from_db()
    assert mock_location.city == "Updated City"
    assert mock_location.state == "SP"


@pytest.mark.django_db
def test_location_delete(mock_client, mock_location):
    url = reverse("locations-detail", args=[mock_location.id])
    response = mock_client.delete(url)
    assert response.status_code == 204

    with pytest.raises(Location.DoesNotExist):
        mock_location.refresh_from_db()
