import pytest
from django.urls import reverse

from src.models import Farmer


@pytest.mark.django_db
def test_farmer_create(mock_farmer_data, mock_client):
    url = reverse("farmers-list")
    response = mock_client.post(url, mock_farmer_data, format="json")
    assert response.status_code == 201

    assert Farmer.objects.count() == 1
    farmer = Farmer.objects.get(id=response.data["id"])
    assert farmer.username == "John Dunha"
    assert farmer.document_type == "CPF"
    assert farmer.document_value == "74744936083"


@pytest.mark.django_db
def test_farmer_retrieve(mock_client, mock_farmer):
    url = reverse("farmers-detail", args=[mock_farmer.id])
    response = mock_client.get(url)
    assert response.status_code == 200
    assert response.data == {
        "id": str(mock_farmer.id),
        "username": "John Dunha",
        "document_type": "CPF",
        "document_value": "74744936083",
    }


@pytest.mark.django_db
def test_farmer_partial_update(mock_client, mock_farmer):
    url = reverse("farmers-detail", args=[mock_farmer.id])
    data = {"username": "John Updated"}

    response = mock_client.patch(url, data, format="json")
    # breakpoint()
    assert response.status_code == 200

    mock_farmer.refresh_from_db()
    assert mock_farmer.username == "John Updated"
    assert mock_farmer.document_type == "CPF"
    assert mock_farmer.document_value == "74744936083"


@pytest.mark.django_db
def test_farmer_update(mock_client, mock_farmer):
    url = reverse("farmers-detail", args=[mock_farmer.id])
    data = {
        "username": "John Updated",
        "document_type": "CNPJ",
        "document_value": "14.963.945/0001-13",
    }

    response = mock_client.put(url, data, format="json")
    assert response.status_code == 200

    mock_farmer.refresh_from_db()
    assert mock_farmer.username == "John Updated"
    assert mock_farmer.document_type == "CNPJ"
    assert mock_farmer.document_value == "14963945000113"


@pytest.mark.django_db
def test_farmer_delete(mock_client, mock_farmer):
    url = reverse("farmers-detail", args=[mock_farmer.id])
    response = mock_client.delete(url)
    assert response.status_code == 204

    with pytest.raises(Farmer.DoesNotExist):
        mock_farmer.refresh_from_db()
