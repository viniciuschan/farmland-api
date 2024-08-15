import pytest

from src.exceptions import InvalidDocumentTypeError
from src.validators import DocumentValidator


@pytest.mark.parametrize(
    "document_value",
    [
        "979.414.340-59",
        "979414340-59",
        "979.414.34059",
        "97941434059",
    ],
)
def test_cpf_validator_is_valid(document_value):
    validator = DocumentValidator("CPF")
    assert validator.validate(document_value) is True


@pytest.mark.parametrize(
    "document_value",
    [
        "0979.414.340-59",
        "979.414.340-590",
        "979.414.340-5",
        "979414340590",
        "9794143405",
    ],
)
def test_cpf_validator_is_invalid(document_value):
    validator = DocumentValidator("CPF")
    assert validator.validate(document_value) is False


@pytest.mark.parametrize(
    "document_value",
    [
        "01.110.919/0001-09",
        "01110919/000109",
        "01.110.9190001-09",
        "01.110.919/000109",
        "01110919000109",
    ],
)
def test_cnpj_validator_is_valid(document_value):
    validator = DocumentValidator("CNPJ")
    assert validator.validate(document_value) is True


@pytest.mark.parametrize(
    "document_value",
    [
        "12345678",
        "1234567890123456",
        "abcdefghijklmno",
    ],
)
def test_cnpj_validator_is_invalid(document_value):
    validator = DocumentValidator("CNPJ")
    assert validator.validate(document_value) is False


def test_invalid_document_type():
    with pytest.raises(InvalidDocumentTypeError):
        DocumentValidator("INVALID_TYPE").validate("12345678901")
