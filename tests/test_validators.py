import pytest

from src.exceptions import InvalidDocumentTypeError
from src.validators import DocumentValidator, FarmValidator


@pytest.mark.parametrize(
    "document_value",
    [
        "979.414.340-59",
        "979414340-59",
        "979.414.34059",
        "97941434059",
    ],
)
def test_document_validator_cpf_is_valid(document_value):
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
def test_document_validator_cpf_is_not_valid(document_value):
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
def test_document_validator_cnpj_is_valid(document_value):
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
def test_document_validator_cnpj_is_not_valid(document_value):
    validator = DocumentValidator("CNPJ")
    assert validator.validate(document_value) is False


@pytest.mark.parametrize(
    "document_type, input_data, expected_output",
    [
        ("CPF", " 747.449.360-83 ", "74744936083"),
        ("CNPJ", " 48.542.058/0001-93 ", "48542058000193"),
    ],
)
def test_document_validator_clean_punctuations(document_type, input_data, expected_output):
    validator = DocumentValidator(document_type)
    cleaned_data = validator.clean_punctuations(input_data)
    assert cleaned_data == expected_output


def test_document_validator_document_type_is_not_valid():
    with pytest.raises(InvalidDocumentTypeError):
        DocumentValidator("INVALID_TYPE").validate("12345678901")


@pytest.mark.parametrize(
    "total_area, cultivable_area, vegetation_area",
    [
        (100, 50, 50),
        (100, 100, 0),
        (100, 0, 100),
        (100, 10, 10),  # there could be some unused area besides the cultivable and vegetation
    ],
)
def test_farmer_validator_validate_areas_is_valid(
    total_area, cultivable_area, vegetation_area, mock_farm_data
):
    mock_farm_data["total_area_hectares"] = total_area
    mock_farm_data["cultivable_area_hectares"] = cultivable_area
    mock_farm_data["vegetation_area_hectares"] = vegetation_area

    validator = FarmValidator(mock_farm_data)
    assert validator.validate_areas() is True


@pytest.mark.parametrize(
    "total_area, cultivable_area, vegetation_area",
    [
        (0, 50, 50),
        (0, 0, 0),
        (100, 150, -50),
        (100, -50, -150),
    ],
)
def test_farmer_validator_validate_areas_is_not_valid(
    total_area, cultivable_area, vegetation_area, mock_farm_data
):
    mock_farm_data["total_area_hectares"] = total_area
    mock_farm_data["cultivable_area_hectares"] = cultivable_area
    mock_farm_data["vegetation_area_hectares"] = vegetation_area

    validator = FarmValidator(mock_farm_data)
    assert validator.validate_areas() is False
